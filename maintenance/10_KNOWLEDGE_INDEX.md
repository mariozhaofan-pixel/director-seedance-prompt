# Runtime Knowledge Index

维护索引，不默认加载。字符数为Unicode文本长度，不代表token数。

| 模块 | 字符数 |
| --- | ---: |
| [00_CORE_CARD](../knowledge/00_CORE_CARD.md) | 3496 |
| [02J_SHOT_CARD](../knowledge/02J_SHOT_CARD.md) | 1773 |
| [02K_PROJECT_SLOT](../knowledge/02K_PROJECT_SLOT.md) | 1782 |
| [02L_PLATFORM_PROFILES](../knowledge/02L_PLATFORM_PROFILES.md) | 512 |
| [01_CORE_EXECUTION_CONTRACT](../knowledge/01_CORE_EXECUTION_CONTRACT.md) | 14264 |
| [01A_SCREENWRITER_HANDOFF](../knowledge/01A_SCREENWRITER_HANDOFF.md) | 2232 |
| [02_REFERENCE_ROUTER_AND_LOCKS](../knowledge/02_REFERENCE_ROUTER_AND_LOCKS.md) | 7392 |
| [02A_PROJECT_WORKFLOW](../knowledge/02A_PROJECT_WORKFLOW.md) | 7092 |
| [02B_CHARACTER_BOARD](../knowledge/02B_CHARACTER_BOARD.md) | 1662 |
| [02C_CONTINUATION_REFERENCES](../knowledge/02C_CONTINUATION_REFERENCES.md) | 4628 |
| [02D_AUDIO_REFERENCES](../knowledge/02D_AUDIO_REFERENCES.md) | 1319 |
| [02E_MEDIA_EVIDENCE](../knowledge/02E_MEDIA_EVIDENCE.md) | 2794 |
| [02F_HIGGSFIELD_ASSET_PREPRODUCTION](../knowledge/02F_HIGGSFIELD_ASSET_PREPRODUCTION.md) | 1575 |
| [02G_IMAGE_CAPABILITY_FALLBACK](../knowledge/02G_IMAGE_CAPABILITY_FALLBACK.md) | 1890 |
| [02H_FEISHU_ASSET_WORKSPACE](../knowledge/02H_FEISHU_ASSET_WORKSPACE.md) | 4028 |
| [03_VISUAL_GRAMMAR_AND_SCENE_ROUTER](../knowledge/03_VISUAL_GRAMMAR_AND_SCENE_ROUTER.md) | 14580 |
| [04_CAMERA_LIGHT_COLOR_STYLE](../knowledge/04_CAMERA_LIGHT_COLOR_STYLE.md) | 23335 |
| [04A_LIVE_ACTION_TEXTURE](../knowledge/04A_LIVE_ACTION_TEXTURE.md) | 2094 |
| [05_ACTION_PERFORMANCE_BODY_MECHANICS](../knowledge/05_ACTION_PERFORMANCE_BODY_MECHANICS.md) | 14945 |
| [05A_COMBAT_EXCHANGE_VARIANTS](../knowledge/05A_COMBAT_EXCHANGE_VARIANTS.md) | 8513 |
| [05B_COMBAT_BRIEF](../knowledge/05B_COMBAT_BRIEF.md) | 1687 |
| [05C_COMBAT_CHOREOGRAPHY](../knowledge/05C_COMBAT_CHOREOGRAPHY.md) | 18764 |
| [05D_ACTION_SCENE_PHYSICS](../knowledge/05D_ACTION_SCENE_PHYSICS.md) | 6478 |
| [05E_EXPRESSION_CUES](../knowledge/05E_EXPRESSION_CUES.md) | 2936 |
| [05F_MARTIAL_STYLES](../knowledge/05F_MARTIAL_STYLES.md) | 12120 |
| [05G_VEHICLE_CINEMA](../knowledge/05G_VEHICLE_CINEMA.md) | 8207 |
| [05H_CHILD_PET_PERFORMANCE](../knowledge/05H_CHILD_PET_PERFORMANCE.md) | 2366 |
| [06_TIMELINE_EDITING_SOUND](../knowledge/06_TIMELINE_EDITING_SOUND.md) | 31270 |
| [06A_COMBAT_TIMING](../knowledge/06A_COMBAT_TIMING.md) | 4299 |
| [06B_TRANSITIONS_SOUND](../knowledge/06B_TRANSITIONS_SOUND.md) | 4642 |
| [07_STYLE_GENRE_FAMOUS_SCENE_COMPILER](../knowledge/07_STYLE_GENRE_FAMOUS_SCENE_COMPILER.md) | 8274 |
| [07A_PAINTING_HOMAGE_ROUTER](../knowledge/07A_PAINTING_HOMAGE_ROUTER.md) | 5266 |
| [08_FAST_PREFLIGHT](../knowledge/08_FAST_PREFLIGHT.md) | 6348 |
| [08_MODEL_QC_REPAIR](../knowledge/08_MODEL_QC_REPAIR.md) | 39608 |
| [STYLE_ROUTER](../knowledge/styles/STYLE_ROUTER.md) | 3464 |
| [bright-ensemble](../knowledge/styles/bright-ensemble/bright-ensemble.md) | 9989 |
| [campus-relationship](../knowledge/styles/campus-relationship/campus-relationship.md) | 8667 |
| [commercial-reversal](../knowledge/styles/commercial-reversal/commercial-reversal.md) | 9669 |
| [phone-vlog](../knowledge/styles/phone-vlog/phone-vlog.md) | 4720 |
| [folk-fantasy-realism](../knowledge/styles/folk-fantasy-realism/folk-fantasy-realism.md) | 19661 |
| [restrained-realism](../knowledge/styles/restrained-realism/restrained-realism.md) | 7317 |

## 内置功能资源

按02F、STYLE_ROUTER或02I触发加载；协议与脚本随Skill提供，角色板细则只有一份。

| 功能 | 文件 |
| --- | --- |
| 静态资产预制及模型路由 | [ASSET_PREPRODUCTION](../capabilities/asset-preproduction/ASSET_PREPRODUCTION.md) |
| 光影运镜表演规则反推 | [REFERENCE_RULE_EXTRACTION](../capabilities/reference-rule-extraction/REFERENCE_RULE_EXTRACTION.md) |
| 完整视频与音频取证 | [VIDEO_EVIDENCE_PROTOCOL](../capabilities/reference-rule-extraction/VIDEO_EVIDENCE_PROTOCOL.md) |
| 媒体脚本运行环境 | [RUNTIME](../capabilities/reference-rule-extraction/RUNTIME.md) |
| 演唱翻唱 | [COVER_PERFORMANCE](../capabilities/cover-performance/COVER_PERFORMANCE.md) |

## 可选飞书工作区资源

只在选择飞书协作时经02H按需读取；本地模式不加载或部署飞书环境。工作模式与规则来源的首轮合并询问由根入口维护。CLI、第三方飞书Skills与凭据独立安装，不随本包分发。

| 资源 | 字符数 | 读取条件 |
| --- | ---: | --- |
| [FEISHU_WORKSPACE_SETUP](../references/FEISHU_WORKSPACE_SETUP.md) | 7063 | 连接器/CLI发现、独立部署、配置授权、密码分享与验证 |
| [FEISHU_BASE_LAYOUT](../references/FEISHU_BASE_LAYOUT.md) | 6311 | 建表映射、修订、关联、视图及专用附件上传下载 |
| [FEISHU_SCREENPLAY_SYNC](../references/FEISHU_SCREENPLAY_SYNC.md) | 2824 | 编剧定稿与采用改稿、当前多批版本、共同工作区恢复及导演交接 |
| [feishu-base-blueprint](../assets/feishu-base-blueprint.json) | 8774 | 创建或增补四表结构时转换为实际请求 |
| [plan_feishu_sync](../scripts/plan_feishu_sync.py) | 16572 | 本地同步计划；计划本身不证明云端已执行 |

## 演唱翻唱

- [02I翻唱接口](../knowledge/02I_COVER_PERFORMANCE.md)：纯演唱与剧情内唱词的条件路由；翻唱能力随包内置并只在本仓库维护，背景配乐不触发；默认采用导演统一五栏。
