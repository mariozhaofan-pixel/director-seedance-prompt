"""Local-only behavioral tests; fixtures are isolated temporary directories."""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import plan_feishu_sync as planner


class SyncPlannerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "project"
        self.root.mkdir()
        self.path = self.root / "提示词.md"
        self.path.write_bytes(b"version one")
        self.field = "对应段落提示词md文件"
        self.sha = hashlib.sha256(self.path.read_bytes()).hexdigest()
        self.request = {
            "kind": "segment", "sync_key": "project/P1/segment/S1/revision/v001",
            "snapshot_complete": True,
            "owned_fields": ["同步键", "名称", "状态", "修订ID", "关联资产", self.field],
            "desired_fields": {"名称": "第001段_开场_v001", "状态": "已编译"},
            "remote_records": [],
            "local_files": [{"field": self.field, "path": self.path.name, "role": "segment_prompt_md"}],
        }

    def attachment(self, content=None, token="token-1"):
        return {"field": self.field, "name": self.path.name,
                "sha256": self.sha if content is None else hashlib.sha256(content).hexdigest(),
                "file_token": token}

    def existing(self, baseline=True):
        remote = {"record_id": "rec-1", "sync_key": self.request["sync_key"],
                  "fields": copy.deepcopy(self.request["desired_fields"]),
                  "files": [self.attachment()]}
        self.request["remote_records"] = [remote]
        if baseline:
            self.request["baseline"] = copy.deepcopy(remote)
        return remote

    def operations(self):
        return planner.plan(self.request, self.root)["operations"]

    def assertNoWrites(self, operations):
        self.assertFalse(any(op["op"] in {"create", "update"} for op in operations))
        self.assertFalse(any("uploads" in op for op in operations))

    def test_create_hashes_actual_bytes_and_adds_stable_key(self):
        original = copy.deepcopy(self.request)
        operations = self.operations()
        self.assertEqual(operations[0]["op"], "create")
        self.assertEqual(operations[0]["fields"]["同步键"], self.request["sync_key"])
        self.assertEqual(operations[0]["uploads"][0]["sha256"], self.sha)
        self.assertEqual(operations[0]["attachment_mode"], "append")
        self.assertEqual(self.request, original)

    def test_incomplete_query_cannot_create_or_update(self):
        for existing in (False, True):
            with self.subTest(existing=existing):
                if existing:
                    self.existing()
                self.request["snapshot_complete"] = False
                operations = self.operations()
                self.assertEqual(operations[0]["op"], "inspect_remote")
                self.assertNoWrites(operations)

    def test_snapshot_completeness_is_explicit(self):
        del self.request["snapshot_complete"]
        with self.assertRaisesRegex(ValueError, "snapshot_complete"):
            self.operations()

    def test_same_hash_real_token_is_noop_even_without_baseline(self):
        self.existing(baseline=False)
        self.assertEqual(self.operations()[0]["op"], "noop")

    def test_same_content_new_token_does_not_reupload(self):
        remote = self.existing()
        remote["files"][0]["file_token"] = "replacement-token"
        self.assertEqual(self.operations()[0]["op"], "noop")

    def test_duplicate_sync_key_cannot_write(self):
        self.existing()
        duplicate = copy.deepcopy(self.request["remote_records"][0])
        duplicate["record_id"] = "rec-2"
        self.request["remote_records"].append(duplicate)
        operations = self.operations()
        self.assertEqual(operations[0]["reason"], "duplicate_sync_key")
        self.assertNoWrites(operations)

    def test_removed_record_is_not_recreated(self):
        self.existing()
        self.request["remote_records"] = []
        self.assertEqual(self.operations()[0]["reason"], "remote_record_removed")

    def test_wrong_baseline_record_blocks_writes(self):
        self.existing()
        self.request["baseline"]["record_id"] = "other-record"
        operations = self.operations()
        self.assertEqual(operations[0]["op"], "conflict")
        self.assertNoWrites(operations)

    def test_wrong_baseline_sync_key_is_rejected(self):
        self.existing()
        self.request["baseline"]["sync_key"] = "wrong-project"
        with self.assertRaisesRegex(ValueError, "baseline sync_key mismatch"):
            self.operations()

    def test_only_local_scalar_change_writes_only_changed_field(self):
        self.existing()
        self.request["desired_fields"]["状态"] = "已交付"
        operations = self.operations()
        self.assertEqual(operations[0]["fields"], {"状态": "已交付"})
        self.assertEqual(operations[0]["uploads"], [])

    def test_remote_scalar_change_pulls(self):
        self.existing()["fields"]["状态"] = "冲突"
        operations = self.operations()
        self.assertEqual(operations[0]["op"], "pull")
        self.assertEqual(operations[0]["fields"], {"状态": "冲突"})
        self.assertTrue(operations[0]["preserve_local"])
        self.assertNoWrites(operations)

    def test_scalar_conflict_blocks_other_pending_local_change(self):
        self.existing()["fields"]["状态"] = "冲突"
        self.request["desired_fields"].update({"状态": "已交付", "名称": "local rename"})
        operations = self.operations()
        self.assertEqual(operations[0]["op"], "conflict")
        self.assertNoWrites(operations)

    def test_new_device_does_not_overwrite_different_remote_scalar(self):
        self.existing(baseline=False)["fields"]["状态"] = "已交付"
        operation = self.operations()[0]
        self.assertEqual(operation["op"], "pull")
        self.assertTrue(operation["preserve_local"])

    def test_missing_baseline_field_is_not_permission_to_overwrite(self):
        self.existing()["fields"]["状态"] = "已交付"
        del self.request["baseline"]["fields"]["状态"]
        self.assertEqual(self.operations()[0]["reason"], "no_common_baseline")

    def test_first_fill_of_cell_omitted_from_snapshot_updates(self):
        for empty, value in ((None, "已交付"), ("", "已交付"), ([], ["已交付"])):
            with self.subTest(empty=empty):
                self.setUp()
                remote = self.existing()
                del remote["fields"]["状态"]
                self.request["baseline"]["fields"]["状态"] = empty
                self.request["desired_fields"]["状态"] = value
                operations = self.operations()
                self.assertEqual(len(operations), 1)
                self.assertEqual(operations[0]["op"], "update")
                self.assertEqual(operations[0]["fields"], {"状态": value})

    def test_empty_desired_value_matches_omitted_remote_cell(self):
        for baseline in (False, True):
            with self.subTest(baseline=baseline):
                self.setUp()
                self.request["owned_fields"].append("任务ID")
                self.existing(baseline=baseline)
                if baseline:
                    self.request["baseline"]["fields"]["任务ID"] = "old-task"
                self.request["desired_fields"]["任务ID"] = ""
                self.assertEqual(self.operations()[0]["op"], "noop")

    def test_omitted_cell_without_baseline_entry_still_pulls(self):
        self.request["owned_fields"].append("任务ID")
        self.existing()
        self.request["desired_fields"]["任务ID"] = "task-7"
        operation = self.operations()[0]
        self.assertEqual(operation["op"], "pull")
        self.assertEqual(operation["reason"], "no_common_baseline")
        self.assertEqual(operation["missing_fields"], ["任务ID"])

    def test_zero_is_a_value_not_an_omitted_cell(self):
        self.request["owned_fields"].append("段号")
        self.existing()
        self.request["baseline"]["fields"]["段号"] = 0
        self.request["desired_fields"]["段号"] = 2
        operations = self.operations()
        self.assertEqual(operations[0]["reason"], "both_changed_field")
        self.assertNoWrites(operations)

    def test_identity_link_first_fill_from_empty_still_requires_revision(self):
        self.existing()
        self.request["baseline"]["fields"]["关联资产"] = []
        self.request["desired_fields"]["关联资产"] = ["asset-revision-1"]
        operations = self.operations()
        self.assertEqual(operations[0]["op"], "revision_required")
        self.assertEqual(operations[0]["field"], "关联资产")
        self.assertNoWrites(operations)

    def test_segment_changed_md_requires_new_revision_and_preserves_video(self):
        remote = self.existing()
        remote["fields"]["备注"] = "user note"
        remote["files"].append({"field": "对应提示词的视频上传", "name": "user.mp4", "file_token": "video"})
        self.path.write_bytes(b"revised prompt")
        operations = self.operations()
        self.assertEqual(operations[0]["op"], "revision_required")
        self.assertNoWrites(operations)
        self.assertNotIn("user note", json.dumps(operations))
        self.assertNotIn("video", json.dumps(operations))
        self.assertEqual(remote["files"][1]["file_token"], "video")

    def test_asset_changed_image_requires_new_revision(self):
        self.request["kind"] = "asset"
        self.request["owned_fields"].remove("关联资产")
        self.request["owned_fields"].remove(self.field)
        self.field = "图片资产"
        self.request["owned_fields"].append(self.field)
        self.request["local_files"][0]["field"] = self.field
        self.existing()
        self.path.write_bytes(b"new image bytes")
        self.assertEqual(self.operations()[0]["op"], "revision_required")

    def test_changed_exact_asset_links_require_revision(self):
        self.request["desired_fields"]["关联资产"] = ["asset-revision-1"]
        self.existing()
        self.request["desired_fields"]["关联资产"] = ["asset-revision-2"]
        self.assertEqual(self.operations()[0]["op"], "revision_required")

    def test_asset_a_cannot_be_turned_into_b_on_existing_row(self):
        key = "project/P1/asset/A1/revision/v001"
        remote = {"record_id": "rec-A1-v1", "sync_key": key, "files": [],
                  "fields": {"方向": ["A"], "空间组ID": "space-1", "名称": "场景_茶室_A_v001"}}
        request = {"kind": "asset", "sync_key": key, "snapshot_complete": True,
                   "owned_fields": ["同步键", "方向", "空间组ID", "名称"],
                   "desired_fields": {"方向": ["B"], "空间组ID": "space-2", "名称": "场景_茶室_B_v001"},
                   "remote_records": [remote], "baseline": copy.deepcopy(remote), "local_files": []}
        operations = planner.plan(request, self.root)["operations"]
        self.assertEqual({op["field"] for op in operations}, {"方向", "空间组ID"})
        self.assertTrue(all(op["op"] == "revision_required" for op in operations))
        self.assertNoWrites(operations)
        self.assertEqual(remote["fields"]["方向"], ["A"])
        self.assertEqual(remote["fields"]["名称"], "场景_茶室_A_v001")

    def test_asset_type_change_blocks_pending_name_update(self):
        key = "project/P1/asset/A1/revision/v001"
        remote = {"record_id": "rec-A1-v1", "sync_key": key, "files": [],
                  "fields": {"类型": ["场景"], "名称": "场景_茶室_A_v001"}}
        request = {"kind": "asset", "sync_key": key, "snapshot_complete": True,
                   "owned_fields": ["同步键", "类型", "名称"],
                   "desired_fields": {"类型": ["角色"], "名称": "角色_茶室_v001"},
                   "remote_records": [remote], "baseline": copy.deepcopy(remote), "local_files": []}
        operations = planner.plan(request, self.root)["operations"]
        self.assertEqual(operations[0]["op"], "revision_required")
        self.assertEqual(operations[0]["field"], "类型")
        self.assertNoWrites(operations)

    def test_project_index_revision_appends(self):
        self.request["kind"] = "project"
        self.request["owned_fields"].remove("关联资产")
        self.request["owned_fields"].remove(self.field)
        self.field = "总索引md文件"
        self.request["owned_fields"].append(self.field)
        self.request["local_files"][0]["field"] = self.field
        remote = self.existing()
        self.path.write_bytes(b"new index")
        operations = self.operations()
        self.assertEqual(operations[0]["op"], "update")
        self.assertEqual(operations[0]["attachment_mode"], "append")
        self.assertEqual(len(operations[0]["uploads"]), 1)
        self.assertEqual(remote["files"][0]["file_token"], "token-1")

    def use_script(self):
        self.field = "剧本md文件"
        self.request = {
            "kind": "script", "sync_key": "project/P1/script/E001/revision/v001",
            "snapshot_complete": True,
            "owned_fields": ["同步键", "名称", "剧本ID", "修订ID", "集场范围", "状态", "所属项目", self.field],
            "desired_fields": {"名称": "第001集_定稿_v001", "剧本ID": "E001", "修订ID": "v001",
                               "集场范围": "第001集全部场次", "状态": "已定稿", "所属项目": ["project-record"]},
            "remote_records": [],
            "local_files": [{"field": self.field, "path": self.path.name, "role": "screenplay_md"}],
        }

    def use_current_scripts(self):
        self.request = {
            "kind": "project", "sync_key": "project/P1", "snapshot_complete": True,
            "owned_fields": ["同步键", "名称", "当前剧本"],
            "desired_fields": {"名称": "第一季", "当前剧本": ["E001-v001", "E002-v001"]},
            "remote_records": [], "local_files": [],
        }
        remote = {"record_id": "project-record", "sync_key": "project/P1",
                  "fields": copy.deepcopy(self.request["desired_fields"]), "files": []}
        self.request["remote_records"] = [remote]
        self.request["baseline"] = copy.deepcopy(remote)
        return remote

    def test_script_create_hashes_final_md_and_preserves_role(self):
        self.use_script()
        operation = self.operations()[0]
        self.assertEqual(operation["op"], "create")
        self.assertEqual(operation["fields"]["同步键"], "project/P1/script/E001/revision/v001")
        self.assertEqual(operation["fields"]["所属项目"], ["project-record"])
        self.assertEqual(operation["uploads"][0]["field"], "剧本md文件")
        self.assertEqual(operation["uploads"][0]["role"], "screenplay_md")
        self.assertEqual(operation["uploads"][0]["sha256"], self.sha)

    def test_script_same_hash_and_real_token_skips_duplicate_upload(self):
        self.use_script()
        self.existing(baseline=False)
        self.assertEqual(self.operations()[0]["op"], "noop")

    def test_script_changed_md_requires_new_revision_and_keeps_original(self):
        self.use_script()
        remote = self.existing()
        before = copy.deepcopy(remote)
        self.path.write_bytes(b"adopted screenplay revision")
        operations = self.operations()
        self.assertEqual(operations[0]["op"], "revision_required")
        self.assertNoWrites(operations)
        self.assertEqual(remote, before)

    def test_script_revision_identity_range_and_project_are_immutable(self):
        for field, value in (("剧本ID", "E002"), ("修订ID", "v002"),
                             ("集场范围", "第002集全部场次"), ("所属项目", ["other-project"])):
            with self.subTest(field=field):
                self.use_script()
                self.existing()
                self.request["desired_fields"][field] = value
                operations = self.operations()
                self.assertEqual(operations[0]["op"], "revision_required")
                self.assertEqual(operations[0]["field"], field)
                self.assertNoWrites(operations)

    def test_script_both_changed_md_conflicts_without_touching_manual_fields(self):
        self.use_script()
        remote = self.existing()
        remote["files"] = [self.attachment(b"remote revised screenplay", "remote-token")]
        remote["fields"]["备注"] = "人工保留备注"
        remote["files"].append({"field": "对应提示词的视频上传", "name": "user.mp4", "file_token": "user-video"})
        self.path.write_bytes(b"local revised screenplay")
        before = copy.deepcopy(remote)
        operations = self.operations()
        self.assertEqual(operations[0]["reason"], "both_changed_attachment")
        self.assertNoWrites(operations)
        self.assertEqual(remote, before)
        self.assertNotIn("user-video", json.dumps(operations))

    def test_script_only_remote_md_changed_pulls_confirmed_revision(self):
        self.use_script()
        self.existing()["files"] = [self.attachment(b"remote revised screenplay", "remote-token")]
        operation = self.operations()[0]
        self.assertEqual(operation["op"], "pull")
        self.assertEqual(operation["files"][0]["file_token"], "remote-token")
        self.assertTrue(operation["preserve_local"])

    def test_script_partial_snapshot_blocks_create_and_update(self):
        for exists in (False, True):
            with self.subTest(exists=exists):
                self.use_script()
                if exists:
                    self.existing()
                    self.request["desired_fields"]["状态"] = "已采用修订"
                self.request["snapshot_complete"] = False
                operations = self.operations()
                self.assertEqual(operations[0]["reason"], "snapshot_incomplete")
                self.assertNoWrites(operations)

    def test_script_cannot_manage_assets_index_video_or_manual_notes(self):
        for field in ("图片资产", "总索引md文件", "对应段落提示词md文件", "对应提示词的视频上传", "备注", "当前文件清单"):
            with self.subTest(field=field):
                self.use_script()
                self.request["owned_fields"].append(field)
                with self.assertRaises(ValueError):
                    self.operations()

    def test_segment_source_script_change_requires_new_revision(self):
        self.request["owned_fields"].append("来源剧本")
        self.request["desired_fields"]["来源剧本"] = ["E001-v001"]
        remote = self.existing()
        remote["files"].append({"field": "对应提示词的视频上传", "name": "user.mp4", "file_token": "old-video"})
        self.request["desired_fields"]["来源剧本"] = ["E001-v002"]
        operations = self.operations()
        self.assertEqual(operations[0]["op"], "revision_required")
        self.assertEqual(operations[0]["field"], "来源剧本")
        self.assertNoWrites(operations)
        self.assertEqual(remote["fields"]["来源剧本"], ["E001-v001"])
        self.assertEqual(remote["files"][1]["file_token"], "old-video")

    def test_current_script_update_accepts_complete_set_with_other_batches_retained(self):
        remote = self.use_current_scripts()
        # The caller resolves script identity/ranges; this row planner receives
        # the full replacement set, including the untouched second batch.
        self.request["desired_fields"]["当前剧本"] = ["E001-v002", "E002-v001"]
        operation = self.operations()[0]
        self.assertEqual(operation["op"], "update")
        self.assertEqual(operation["fields"], {"当前剧本": ["E001-v002", "E002-v001"]})
        self.assertEqual(remote["fields"]["当前剧本"], ["E001-v001", "E002-v001"])

    def test_current_script_pointer_omitted_means_untouched(self):
        remote = self.use_current_scripts()
        del self.request["desired_fields"]["当前剧本"]
        self.request["desired_fields"]["名称"] = "第一季定稿"
        operation = self.operations()[0]
        self.assertEqual(operation["fields"], {"名称": "第一季定稿"})
        self.assertEqual(remote["fields"]["当前剧本"], ["E001-v001", "E002-v001"])

    def test_current_script_concurrent_batch_change_blocks_overwriting_other_batch(self):
        remote = self.use_current_scripts()
        remote["fields"]["当前剧本"] = ["E001-v001", "E002-v002"]
        self.request["desired_fields"]["当前剧本"] = ["E001-v002", "E002-v001"]
        self.request["desired_fields"]["名称"] = "pending local rename"
        operations = self.operations()
        self.assertEqual(operations[0]["reason"], "both_changed_field")
        self.assertEqual(operations[0]["field"], "当前剧本")
        self.assertNoWrites(operations)

    def test_current_script_no_common_baseline_cannot_overwrite(self):
        self.use_current_scripts()
        del self.request["baseline"]["fields"]["当前剧本"]
        self.request["desired_fields"]["当前剧本"] = ["E001-v002", "E002-v001"]
        operations = self.operations()
        self.assertEqual(operations[0]["reason"], "no_common_baseline")
        self.assertNoWrites(operations)

    def test_current_script_partial_snapshot_blocks_pointer_update(self):
        self.use_current_scripts()
        self.request["desired_fields"]["当前剧本"] = ["E001-v002", "E002-v001"]
        self.request["snapshot_complete"] = False
        operations = self.operations()
        self.assertEqual(operations[0]["reason"], "snapshot_incomplete")
        self.assertNoWrites(operations)

    def test_remote_attachment_change_pulls_actual_token(self):
        self.existing()["files"] = [self.attachment(b"remote version", "token-2")]
        operations = self.operations()
        self.assertEqual(operations[0]["op"], "pull")
        self.assertEqual(operations[0]["files"][0]["file_token"], "token-2")
        self.assertTrue(operations[0]["preserve_local"])

    def test_new_device_different_attachment_conflicts_and_keeps_both(self):
        self.existing(baseline=False)["files"] = [self.attachment(b"remote version")]
        operations = self.operations()
        self.assertEqual(operations[0]["op"], "conflict")
        self.assertEqual(operations[0]["reason"], "no_common_attachment_baseline")
        self.assertEqual(operations[0]["files"][0]["file_token"], "token-1")
        self.assertEqual(self.path.read_bytes(), b"version one")
        self.assertNoWrites(operations)

    def test_missing_attachment_baseline_conflict_blocks_scalar_writes(self):
        self.existing()["files"] = [self.attachment(b"remote version")]
        self.request["baseline"]["files"] = []
        self.request["desired_fields"]["状态"] = "已交付"
        operations = self.operations()
        self.assertEqual(operations[0]["op"], "conflict")
        self.assertNoWrites(operations)

    def test_empty_local_files_does_not_request_bootstrap_download(self):
        self.existing(baseline=False)
        self.request["local_files"] = []
        self.assertEqual(self.operations()[0]["op"], "noop")

    def test_both_changed_attachment_conflicts(self):
        self.existing()["files"] = [self.attachment(b"remote version")]
        self.path.write_bytes(b"local version")
        self.assertEqual(self.operations()[0]["op"], "conflict")

    def test_unknown_remote_hash_blocks_all_writes(self):
        self.existing()["files"][0]["sha256"] = None
        self.request["desired_fields"]["状态"] = "已交付"
        operations = self.operations()
        self.assertEqual(operations[0]["op"], "inspect_remote")
        self.assertNoWrites(operations)

    def test_removed_remote_attachment_pulls_or_conflicts_never_uploads(self):
        remote = self.existing()
        for removed in ([], [self.attachment(token=None)]):
            for changed in (False, True):
                with self.subTest(removed=removed, changed=changed):
                    remote["files"] = removed
                    self.path.write_bytes(b"local new" if changed else b"version one")
                    operations = self.operations()
                    self.assertEqual(operations[0]["op"], "conflict" if changed else "pull")
                    if not changed:
                        self.assertTrue(operations[0]["preserve_local"])
                    self.assertNoWrites(operations)

    def test_missing_token_without_baseline_requires_inspection(self):
        self.existing(baseline=False)["files"][0]["file_token"] = None
        self.assertEqual(self.operations()[0]["op"], "inspect_remote")

    def test_genuinely_empty_attachment_slot_can_be_filled(self):
        self.existing(baseline=False)["files"] = []
        operations = self.operations()
        self.assertEqual(operations[0]["op"], "update")
        self.assertEqual(len(operations[0]["uploads"]), 1)

    def test_unsafe_and_outside_paths_are_rejected(self):
        for path in ("../outside.md", "..\\outside.md", "C:\\secret.md", "\\\\server\\file.md", "/absolute.md", "file.md:stream"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                self.request["local_files"][0]["path"] = path
                self.operations()

    def test_symlink_escape_is_rejected_where_supported(self):
        outside = Path(self.temp.name) / "outside.md"
        outside.write_bytes(b"outside")
        link = self.root / "link.md"
        try:
            link.symlink_to(outside)
        except OSError as error:
            self.skipTest("symlink unavailable: " + str(error))
        self.request["local_files"][0]["path"] = link.name
        with self.assertRaises(ValueError):
            self.operations()

    def test_duplicate_local_field_and_role_are_rejected(self):
        self.request["local_files"].append(copy.deepcopy(self.request["local_files"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate local attachment"):
            self.operations()
        self.request["kind"] = "asset"
        self.request["owned_fields"] = ["同步键", "名称", "状态", "图片资产", "对应图片生成提示词md文件"]
        self.request["local_files"][0]["field"] = "图片资产"
        self.request["local_files"][1]["field"] = "对应图片生成提示词md文件"
        with self.assertRaisesRegex(ValueError, "duplicate local role"):
            self.operations()

    def test_duplicate_current_remote_file_is_rejected(self):
        self.existing()["files"].append(self.attachment(token="second"))
        with self.assertRaisesRegex(ValueError, "duplicate current attachment"):
            self.operations()

    def test_protected_columns_cannot_be_owned_or_written(self):
        for field in ("对应提示词的视频上传", "备注", "当前文件清单", "未知附件列"):
            with self.subTest(field=field):
                request = copy.deepcopy(self.request)
                request["owned_fields"].append(field)
                request["desired_fields"][field] = []
                with self.assertRaises(ValueError):
                    planner.plan(request, self.root)
                request = copy.deepcopy(self.request)
                request["local_files"][0]["field"] = field
                with self.assertRaises(ValueError):
                    planner.plan(request, self.root)

    def test_caller_cannot_supply_a_fake_local_hash(self):
        self.request["local_files"][0]["sha256"] = "0" * 64
        with self.assertRaises(ValueError):
            self.operations()

    def test_cli_works_with_utf8_stdin_and_rejects_duplicate_json_keys(self):
        command = [sys.executable, str(Path(planner.__file__)), "--project-root", str(self.root)]
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        completed = subprocess.run(command, input=json.dumps(self.request, ensure_ascii=False).encode(),
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, check=False)
        self.assertEqual(completed.returncode, 0, completed.stderr.decode())
        self.assertEqual(json.loads(completed.stdout)["operations"][0]["op"], "create")
        invalid = subprocess.run(command, input=b'{"kind":"asset","kind":"project"}',
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, check=False)
        self.assertEqual(invalid.returncode, 2)
        self.assertIn("duplicate JSON key", json.loads(invalid.stdout)["error"])

    def test_cli_help_is_utf8_and_exposes_schema_and_whitelist(self):
        completed = subprocess.run([sys.executable, str(Path(planner.__file__)), "--help"],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
                                   env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
        self.assertEqual(completed.returncode, 0)
        help_text = completed.stdout.decode("utf-8")
        self.assertIn("snapshot_complete", help_text)
        self.assertIn("来源A", help_text)
        self.assertIn("协作约定", help_text)
        self.assertIn("screenplay_md", help_text)
        self.assertIn("当前剧本", help_text)
        self.assertIn("来源剧本", help_text)


class SharedScreenplayBlueprintTests(unittest.TestCase):
    def test_four_table_blueprint_resolves_views_and_preserves_managed_roles(self):
        path = Path(planner.__file__).resolve().parent.parent / "assets" / "feishu-base-blueprint.json"
        blueprint = json.loads(path.read_text(encoding="utf-8"))
        tables = {table["table_ref"]: table for table in blueprint["tables"]}
        self.assertEqual(blueprint["schema_version"], "2.0.0")
        self.assertEqual(blueprint["table_order"], ["projects", "assets", "segments", "scripts"])
        self.assertEqual(set(tables), set(blueprint["table_order"]))
        columns = {ref: {field["name"] for field in table["fields"]} for ref, table in tables.items()}
        for link in blueprint["deferred_links"]:
            field = link["field"]
            columns[link["source_table_ref"]].add(field["name"])
            self.assertIn(field["table_ref"], tables)
            if field["bidirectional"]:
                columns[field["table_ref"]].add(field["bidirectional_link_field_name"])
        for ref, table in tables.items():
            for view in table["views"]:
                self.assertLessEqual(set(view["visible_fields"]["visible_fields"]), columns[ref])
        contract = blueprint["record_contract"]
        self.assertEqual(contract["file_roles"]["projects"], {"project_index_md": "总索引md文件"})
        self.assertEqual(contract["file_roles"]["scripts"], {"screenplay_md": "剧本md文件"})
        self.assertIn("当前剧本", columns["projects"])
        self.assertIn("剧本历史", columns["projects"])
        self.assertIn("来源剧本", columns["segments"])
        self.assertEqual(contract["excluded_from_record_write_payloads"], ["对应提示词的视频上传", "备注"])


if __name__ == "__main__":
    unittest.main()
