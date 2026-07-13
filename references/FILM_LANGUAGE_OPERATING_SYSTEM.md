# Film Language Operating System

This is the single operating knowledge base for the director-seedance-prompt skill. Use it to make AI think like a director: Story -> Director -> Storyboard -> Prompt -> Video.

## 0. Operating Contract

The output is not decorative prose. It is a directable film plan and model-executable prompt system.

Visible output contract:

- Default final output is Chinese, clear, and copy-ready.
- Do not expose internal library names, test cases, retrieval notes, or English template headings unless the user asks for analysis.
- User-facing segment titles should be Chinese, such as `### 第01段｜8-15秒｜[场景功能]`.
- Do not output `Segment 01`, `Shot 01`, `STYLE LOCK`, `VISUAL ANCHOR`, `CAMERA/LENS LOOK`, or `Prompt:` as visible headings.
- Use English only as short technical terms inside Chinese sentences when it reduces model ambiguity, such as `slow dolly in`, `rack focus`, `screen-left`, or `foreground`.

Non-negotiable rules:

- One storyboard beat = one primary information unit. One Seedance model segment = a packed generation unit that may contain several compatible beats.
- Every cut must have a reason: information change, emotional change, viewpoint change, conflict escalation, scale reveal, or action-result confirmation.
- Shot/beat duration must be earned by story function, information density, shot scale, motion intensity, continuity need, emotional hold, sound bridge, and Seedance limits. Do not apply fixed second buckets mechanically.
- Seedance segment duration target is `5-15s`, preferably `12-15s` when the story, space, speaker, and action are continuous.
- Every action must include spatial relationship, contact point or force source, failure risk, result, and sound confirmation.
- Every action conflict must behave as an exchange: route -> threat -> evade/block/contact -> counterforce -> escalation/charge -> decisive contact -> aftermath.
- Every lighting description must include source, direction, intensity, shadow behavior, and material reaction. Never write only "warm light" or "cold light".
- Every camera style must be translated into visible image qualities. Do not only write camera/lens names.
- Every camera movement must serve story function: reveal scale, shift power, express realization, preserve action continuity, distort time, or change emotional pressure.
- Before choosing a camera trick, route the scene by function: dialogue power, confession, investigation, suspense search, threat entrance, chase, rescue, fight, disaster warning, scale awe, social pressure, memory, montage, transformation, comedy delay, product/craft process, sports broadcast, vehicle danger, long-take route, reversal reveal, or aftermath.
- Famous scene references must be translated into original scene grammar. Do not copy protected characters, dialogue, exact blocking, set dressing, or franchise identifiers unless the user provides authorized references and explicitly requests that workflow.
- Actor emotion is decided internally through objective, obstacle, tactic, beat reversal, face, breath, body, rhythm, and mask-vs-leak behavior; visible Chinese output should write these as 目标、阻碍、策略、节拍反转、面部、呼吸、身体、节奏、表面控制与真实泄露。
- Visual impact and reversal must change audience knowledge, character knowledge, conflict state, spatial scale, or consequence.
- Every Seedance-oriented prompt uses a two-level visual lock: `【基础风格】` first locks camera/lens style, focal/depth feel, lighting motivation, contrast, palette/LUT, atmosphere, and material reaction; `【运镜与时间轴】` then integrates frame structure, composition, focus path, camera movement, action timing, and ending state per time beat.
- `【基础风格】` is not a mood label. It is the segment-level photography and lighting decision translated into visible image qualities. It appears in every independent segment, repeats the project-level visual baseline, and adds only the scene-specific shift.
- When motion matters, body action must be decomposed into visible body-part mechanics, preferably in Chinese visible wording: 头/眼、肩、肘、手腕/手、躯干、腰/髋、膝、脚、重心变化、接触点、反作用、恢复姿态。
- Every crowd must have main direction, counter direction if any, congestion point, and escape or flow route.
- Expression and body action are separate layers: `deadpan face + fast purposeful walk`.
- Before delivering Seedance prompts, run a stability gate: re-anchor positions after cuts, use one primary camera move per beat, name fixed vs moving objects, limit tracked subjects, and flag reflection/text/crowd/multi-instance risks.
- Seedance hard rule: each segment `<=15s`, `<=10000 characters`, independently complete, repeat anchors in every segment; do not create sub-5-second segments unless a strong boundary requires it.
- Sequence rule: plan the whole story, but compile only the current unresolved Seedance segment. Continuation, next-part, extend, and repair-tail prompts must start from accepted footage, an accepted final frame, or an exact visible-end description; never from an assumed planned ending.
- Beat firewall: silently classify beats as already happened, this segment only, reserved for later, or do not show yet. Already-happened beats must not replay, and reserved future beats must not leak into the current prompt.
- Prompt-budget rule: one generation has finite capacity. Before drafting, choose one primary spend among identity fidelity, motion boldness, or scene density, choose at most one secondary spend, and simplify or split everything else.

## 0A. Seedance Silent Prompt Craft Contract

Use this contract when compiling for Seedance or when the user gives Seedance prompt rules, reference images, sequence frames, storyboards, existing prompts, or prompt templates.

Core identity:

- The system thinks as `Story -> Director -> Storyboard -> Prompt`, but the visible output is still prompt text unless the user asks to see analysis.
- The prompt must not read like keyword stuffing. It must read like a director and cinematographer giving executable instructions to a video model.
- The director logic must be visible inside the prompt through scene lock, camera grammar, action blocking, time axis, sound binding, ending state, and constraints.

Language and ambiguity rules:

- Write primarily in Chinese.
- Add English only when it prevents ambiguity in camera movement, shot grammar, body blocking, continuity, subject count, or model behavior.
- Useful English locks include: `continuous long take`, `one continuous shot`, `ENG news camera`, `lateral tracking shot`, `lateral truck`, `slow push-in`, `slow dolly in`, `rack focus`, `slow motion`, `low-frequency rumble`, `a single three-headed hellhound`, `three heads on one shared body`.
- Prefer positive executable wording. Express one idea once.
- Put negative requirements at the end under `【画面清洁与限制】`; do not scatter many negative clauses through the main prompt.

Seedance duration and independence:

- One Seedance prompt segment must be `<=15s` and `<=10000 characters`; target `5-15s`, preferably near `15s` when continuity allows.
- Multi-segment output must make every segment copyable alone. Never write "延续上一段", "承接上一镜", "同上设定不变", or any dependency on hidden context.
- Each segment must restate scene, character, subject appearance, costume, key props, style, camera movement, action, dialogue, sound, visual cleanliness, and continuity state.
- If crowds, background people, bystanders, lines, herds, or background extras appear, each segment and each WS/EWS/wide beat must restate their density, screen layer, flow direction, congestion point, and visibility. Soft blur is allowed, but background people remain visible unless their exit, dispersal, occlusion, or crop-out is explicitly described.
- If a user explicitly demands one single Seedance video longer than 15 seconds, ask whether to compress into 15 seconds or split into multiple segments. If they ask for a finished deliverable and do not forbid splitting, split automatically.
- Distinguish storyboard cuts from Seedance segments. Do not output one prompt block per storyboard shot by default. Pack adjacent storyboard beats into one Seedance prompt when they share the same location, same primary character or speaker, and one continuous action/dialogue chain. Split early only for scene/location change, disruptive shot-scale or camera setup change, primary character/speaker change, time-state change, or the end of a causal action unit. Inside one Seedance prompt, use one continuous shot or 3-6 internal time beats with simple, motivated cut markers.
- Adjacent independent segments should not end and start on the same character with the same shot scale and composition. Open the next segment with a changed shot scale, camera angle, subject, action state, spatial scale, or information focus. Do not force mask/fabric-wipe/foreground-occlusion transitions between segments unless a real story object naturally crosses the lens.

Default complete Seedance structure:

```text
### 【Seedance 完整提示词】
【基础风格】
【角色/场景/素材锁定】
【运镜与时间轴】
【声音设计】
【画面清洁与限制】
```

Do not output standalone `【台词】`, `【台词/旁白】`, `【打斗提示词】`, `【招式说明】`, or default `【动作调度】` sections. Dialogue, narration, martial choreography, body mechanics, weapon contact, energy collision, internal OS, and off-screen voice must be placed inside the matching `【运镜与时间轴】` time beat with exact timing and visible state.

Always auto-fill `【基础风格】` for cinematic video prompts. Choose camera/lens style by subject and atmosphere, then translate equipment into visible image qualities: dynamic range, highlight behavior, shadow depth, skin tone, depth of field, lighting, color, and genre mood. Do not write equipment names as decoration.

`【基础风格】` must carry the high-priority camera and lighting lock for the whole segment:

```text
摄影机/镜头质感: camera family or visible image qualities, lens group or lens feel, focal/depth behavior, format/aspect feel.
光线设计: motivated source, direction, intensity, contrast ratio feel, shadow behavior, atmosphere, material reaction.
色彩/LUT: palette, warm/cool relationship, saturation, highlight/shadow color, LUT language when useful.
艺术风格转译: if user names a painter, art movement, illustration style, or style image, translate it into visible line, color, composition, texture, light, mood, and use case; do not rely on the artist/style name alone.
类型质感: documentary, high-end drama, epic widescreen, procedural tension, sci-fi night, disaster realism, etc.
```

Visual style descriptor compression:

```text
VISUAL STYLE DESCRIPTOR: [style source] -> line [hard/soft/decorative/ink/contour], color [palette/saturation/contrast], composition [poster/flat/depth/symmetry/negative space], texture [oil/watercolor/ink/digital/film grain/paper], light [classical chiaroscuro/impressionist light/flat graphic/cinematic], mood [dream/quiet/epic/absurd/warm], use case [character/landscape/product/sci-fi/animation].
```

Use style references inside `【基础风格】` only. They must not override camera/lens choice, lighting motivation, scene facts, character identity, action, or timeline.

Recommended output priority for Seedance complete prompts:

```text
【基础风格】camera/lens + lighting/color lock
-> 【角色/场景/素材锁定】character + scene + props + reference roles + audio/voice anchors with short locked names
-> 【运镜与时间轴】time beats integrating duration rationale, frame structure/composition, focus path, camera movement, martial choreography/body mechanics, action timing, contact/recoil/recovery, dialogue/narration timing with speaker and lip-sync state, marker, sound cue, cut reason, and ending state
-> 【声音设计】
-> 【画面清洁与限制】
```

Seedance anti-misread rules:

- Avoid abstract metaphors that have no visible behavior.
- Convert abstraction into visible face, visible body action, light change, environment change, or camera movement.
- For Seedance, mentally compile frame structure and focus path before writing `【运镜与时间轴】`, then place those details inside the relevant time beats instead of defaulting to separate `【画面结构与构图】`, `【焦点路径】`, or `【结尾状态】` sections.
- After `【基础风格】` locks the global camera/lens and lighting look, write visible image structure inside the timeline before mood language: screen-left/right, foreground/midground/background, focus starts where, focus transfers where, and which object stays fixed.
- Treat screen-left/right and foreground/background as model-facing constraints, not optional cinematography jargon.
- Treat duration as a readability constraint, not a decorative rhythm label. Put the concrete reason for each beat length inside `【运镜与时间轴】`: impact, clue, posture scan, dialogue, atmosphere, emotional hold, long-take immersion, or sound bridge.
- If a subject enters frame, specify side, depth plane, travel direction, destination, and what stays fixed.
- If focus changes, name both subjects: `rack focus from foreground gloved hand to background fixed metal pipe`.
- Avoid relying on vague Chinese phrases such as "镜头推进", "人物挣扎", "构图高级", or "氛围压迫" without concrete frame layout, body mechanics, and camera behavior.
- Avoid multi-character precision action happening at the same time. Give the main character priority; secondary characters react with simple readable actions.
- Avoid critical dependence on exact screen text, signs, posters, subtitles, or dense UI text. If text is necessary, use short, large, centered words in a single position.
- Avoid vague Chinese movement words when they can be misunderstood. Write the Chinese meaning and add a precise English camera/action term.

User-preservation rules:

- Preserve user-specified duration, aspect ratio, language, "no subtitles", "no BGM", exact dialogue, fixed scene facts, and reference-image purpose.
- If the user says "不要字幕，只要台词", do not mention subtitles; write only spoken dialogue.
- Do not add BGM unless requested. If the user says no BGM, write: `无背景音乐，只保留现场声、动作声、环境声。`
- For partial revisions, keep the original prompt's structure, narrative, style, characters, dialogue, spatial relationship, and time rhythm; change only the requested problem.

Reference image handling:

- Translate key visual features into concise stable text: facial features, face shape, hair style/color, costume, weapon/prop, body proportion, main color, silhouette, and identity marks.
- For multiple images, videos, or audio files, assign roles before writing the prompt. This is the same principle as scene lock and character lock: every `@` reference must explain its purpose.
- For images, assign roles: character identity anchor, creature/prop anchor, armor/weapon anchor, first-frame anchor, final-frame anchor, scene anchor, color/style anchor.
- For videos, assign roles: camera path, action choreography, edit rhythm, VFX/transition behavior, sound reference, or continuity reference. Do not let a reference video overwrite character, costume, scene, story, or dialogue unless explicitly assigned.
- For audio, assign roles: BGM, beat grid, ambience, SFX, voice tone, narrator voice, or character voice. If an audio clip is used as a voice reference, lock it as a reusable voice identity across segments.
- For Seedance, an audio reference may be a silent motion-control track rather than final soundtrack. If the user wants the audio to control rhythm only, write that @Audio controls beat grid, motion accents, impact timing, cut timing, or camera-speed feel only; it must not be output as final BGM/dialogue/SFX unless assigned.
- Deeply inspect the reference image before using it: subject identity, age, costume, props, environment, period, weather, lighting, palette, composition, action state, camera angle, and what is outside the image's evidence.
- Compare the image against the script or prompt. If there is a major conflict, such as different character age/gender, wrong setting, wrong vehicle/prop, incompatible action state, different era, or scene geography that breaks the plot, stop and ask the user to choose one route:
  1. Preserve the reference image and modify the story/prompt to match the image.
  2. Preserve the story/prompt and generate a new image-generation prompt to replace the image.
- If the conflict is minor, state the assumption briefly and borrow only the useful anchors.
- If the user asks to fully follow an uploaded image, state that the character keeps the reference image's core facial features, face shape, hairstyle, and identity markers through the whole segment.
- Separate what is borrowed from what is not borrowed only when the risk is concrete. A tattoo, armor design, weapon, pose, or color reference must not accidentally overwrite facial identity.

Reference dimension lock:

Default user-facing behavior: place reference usage, character identity, scene identity, props, and voice/audio anchors together inside `【角色/场景/素材锁定】`. State what each reference controls, assign a short locked name, and do not list every "does not control" clause unless ambiguity, multi-reference conflict, protected identity/brand/voice, audio leakage, or visible drift risk would hurt generation. Keep the full exclusion logic silently even when the user-facing prompt stays concise. Once a reference has a locked name, timeline beats use that name instead of repeatedly writing `@ImageN/@VideoN/@AudioN`.

```text
REFERENCE DIMENSION LOCK:
@ImageN controls [identity/costume/scene/prop/color/first frame/final frame] only.
@VideoN controls [camera path/action choreography/edit rhythm/VFX transition/sound] only.
@AudioN controls [BGM/silent beat guide/motion rhythm/impact timing/cut markers/camera-speed feel/ambience/SFX/voice tone/narrator voice/character voice] only.
Silent rule: all unassigned dimensions remain controlled by the user's script and current segment locks.
Visible exclusions: write "does not control..." only when the risk is concrete.
Naming rule: after the lock section, use names like Character A, Scene A, Voice A, Action Reference A, or the Chinese equivalents 主角A / 场景A / 声线A / 动作参考A inside the timeline.
```

Audio / voice lock:

```text
AUDIO VOICE LOCK: use @AudioN or @VideoN audio as [character/narrator] voice reference; preserve [gender/age range/timbre/accent/emotional delivery/speaking pace] across all segments where that character speaks. Voice reference controls sound only, not face, costume, setting, or dialogue content. Voiceover/internal narration must not create visible lip-sync unless the character is speaking on screen.
```

Audio-to-motion beat control:

Use this when a reference audio is provided to shape Seedance motion, action rhythm, camera rhythm, or cut rhythm.

- First choose the audio role: final BGM, silent beat guide, SFX guide, ambience bed, or voice anchor.
- If the audio is only a silent beat guide, explicitly separate input control from output sound: `@AudioN controls motion rhythm and cut markers only; do not output this reference audio as background music; final sound uses [现场声/动作声/用户指定BGM].`
- Use custom SFX/beat grids when the goal is precise fight rhythm, speed changes, impact timing, or camera accents. Use final music when the goal is matching an already chosen BGM style.
- Treat beat landing as guidance, not deterministic frame-locking. Name 3-6 major beat markers in `【运镜与时间轴】`; do not ask Seedance to obey dense sub-frame audio edits.
- Keep story clarity above beat matching. If the music pushes the shot toward dance, close-ups, or long emotion holds, re-anchor the action route, contact point, ending state, and no-output audio rule.
- If the audio purpose is ambiguous, route full music/song/score as `final BGM + beat grid`; route drum hits, wind whooshes, short SFX, or edit beat tracks as `silent beat guide / SFX guide`. If the user says no BGM, the no-BGM instruction wins and the reference audio becomes a silent beat guide.
- Do not let later sound wording contradict the audio lock. If @Audio is a silent beat guide, `【声音设计】` or SOUND DRAMATURGY must not say that same reference audio plays as background music.

Observed Seedance audio bias patterns:

| Audio cue | Likely visual bias | Prompt-side use |
|---|---|---|
| wind whoosh / swish | fast movement, dash, speed-line feel, camera sweep | map to evasion, rush, lateral move, whip pan, cloak/cloth snap |
| drum hit / hard transient | heavy impact, hard cut, cut-in close-up, contact emphasis | place on punch, collision, weapon contact, foot stomp, door slam |
| repeated fast transients | rapid combo, strobing close-ups, accelerated exchange | use for short action chain; keep subject count low |
| sustained strings / pad | emotional hold, long shot, slow push, lyrical pause | use for reaction, realization, farewell, scale reveal |
| piano / waltz-like pulse | footwork, continuous steps, elegant movement, dance-like fight | use for pursuit, duel footwork, ritual, product glide |
| rock / strong backbeat | stronger hit feel, more close-ups, aggressive cut-ins | use for impact-heavy action; warn against over-cutting |
| fast electronic beat | two-subject readable frame, observer/game feel, medium impact | use for clean action readability or MV/montage pacing |

Prompt kernel:

```text
AUDIO RHYTHM LOCK: @AudioN is a [silent beat guide / final BGM / SFX guide / ambience bed / voice anchor]. It controls [beat grid / motion accents / impact timing / cut markers / camera-speed feel] only; [state whether it is output or not]. In 【运镜与时间轴】, align major action markers to [0.0s cue], [x.xs cue], [y.ys cue], while keeping story action, contact points, and ending state readable.
```

Prompt-template learning:

- When the user gives a reference prompt or says "学习这个结构", learn the structure, expression style, and content framework.
- Do not copy the reference prompt's specific subject, character, monster, mecha, weapon, scene, plot, color, or effect unless explicitly requested.
- Replace all story content with the current task while preserving the useful skeleton.

Sequence-frame / storyboard / keyframe handling:

- Treat continuous screenshots, storyboard panels, action references, and video keyframes as action, camera, rhythm, and director-thinking templates.
- Processing order: evidence review -> true cuts vs same-shot continuations -> continuous action -> body mechanics -> camera rhythm -> director logic -> executable prompt.
- If the user only wants action description, output body path, center-of-gravity change, limb coordination, speed feel, air pressure, impact feel, and recovery pose.
- If the user wants complete prompt output, include sequence-frame breakdown, learnable director/action logic, and the optimized complete prompt.
- If updating an existing prompt from images, preserve the core prompt setting and integrate only useful action, camera, composition, and director logic from the images.
- Treat automatic scene detection or rough storyboard panels as candidate structure, not truth. Verify edit points by visual evidence when source frames or video are available.
- One actual cut should usually get one distinct storyboard panel. Do not merge true cuts just because the narrative beat is continuous.
- Same-shot continuation is not a new cut. If the camera keeps rolling and only body position changes, preserve it as one continuous shot or one time-axis beat.

Completed short-drama project pattern:

- When reverse-engineering a source video, prefer frame-by-frame or dense contact-sheet evidence over broad plot inference.
- Keep a reference hierarchy:
  - source video / sequence frames: true cut points, action timing, body continuity, camera rhythm.
  - storyboard board: shot order, left/right axis, entry direction, body placement, foreground/midground/background, camera movement arrows, emotional beat order.
  - scene photos: location material, lighting, props, set dressing, weather, color, real-world detail.
  - character photos: face, hair, costume, silhouette, identity marks.
  - text prompt / user correction: naming, language, dialogue, story facts, forbidden elements.
- If storyboard board and scene photos conflict, do not let the board overwrite the scene detail. The board controls spatial relationships; scene photos and text locks control concrete set reconstruction.
- Colored arrows or marks on a storyboard are semantic instructions only: red = body/action direction, blue = camera movement, green = spatial anchors/axis/depth, orange = light direction, yellow = subjective pressure or internal state. Do not render arrows, labels, UI, panel borders, rough sketch texture, or storyboard annotations in the final video.
- If a user gives shot-level corrections, treat them as authoritative: first/last panel, entry side, screen side, no vehicles, no black end card, language rules, and exact character names must propagate into prompts, boards, and constraints.

Continuous-action across cuts:

- If walking, hand-holding, pulling, combat, falling, or carrying continues through cuts, write that the body momentum continues and the step does not stop at the cut.
- For hand-holding or pulling: lock grip point, leading character, following character, relative half-step distance, and continuous walking vector.
- A cut may change scale or viewpoint, but it must not reset feet, hands, eye line, or body direction unless the story requires a reset.
- Useful wording: `steps continue through the cut`, `hand grip remains connected`, `no frozen pose at the cut`, `the same walking vector continues`.

Voice / language / mouth separation:

- Lock who can speak, in which language, and whether the voice is diegetic spoken dialogue, internal OS, narration, or off-screen sound.
- Internal OS or voiceover must not create lip-sync. Write: `Chinese male internal voiceover, lips do not move`.
- If a body is only performing while a different voice carries thought, write: body performs silently; eyes, breath, hand stiffness, shoulders, and timing carry the reaction.
- If a character is locked to a language, repeat it in every independent segment. Example: Korean character speaks Korean only; Chinese lines are male internal OS only.

Audio reverse-analysis fallback:

- Do not invent a music title. If recognition is not reliable, state that no title is confirmed and provide usable sound-design descriptors.
- Break sound into layers: music bed / drone, impact or contact SFX, environment ambience, dialogue, internal OS, sound bridge, silence.
- Useful short-drama sound descriptors: `dark synth drone`, `cinematic tension pulse`, `sub boom`, `reverse riser`, `electric crackle`, `thunder crack`, `urban rain fight foley`, `studio ambience`, `romcom awkward touch sting`.

Action prompt rules:

- Describe body process, not only result.
- Include setup, center of gravity, limb path, prop change, contact point, environment reaction, opponent reaction, recovery pose, and dialogue connection when relevant.
- Replace generic action verbs with body mechanics when motion is important: head/eyes, shoulder line, elbow angle, wrist/hand grip, torso twist, hip/waist rotation, knee bend, foot placement, weight transfer, contact point, recoil, and recovery pose.
- For walking, backing up, falling, struggling, striking, grabbing, or turning, state which body part initiates the motion and which object or ground point receives the force.
- For wuxia/game/combat motion, include crouched loading, ground push-off, fabric/hair force response, shoulder-waist-hip linkage, weapon arc, landing absorption, dust/water shock rings, and post-hit recovery.
- For large monsters, crowds, multiple heads, or multiple limbs, hard-lock numbers and visibility. Example: `a single three-headed hellhound`, `three clear heads on one shared body`, `all three heads visible at the same time`.

Emotion close-up rules:

- Split expression and body. Write visible micro-actions: eyes, breathing, tear line, mouth corner, brow tension, shoulder/neck.
- Build a time axis for emotional change: initial restraint -> middle loss of focus -> late quiet collapse.
- Useful locks: `silent crying`, `restrained sobbing`, `tearful hollow eyes`, `downcast gaze`, `broken but quiet sadness`, `emotionally exhausted`, `quiet collapse`.
- Avoid sudden broad gestures, melodramatic sobbing, or emotional jumps unless the user asks.

Mecha / armor / transformation rules:

- Transformation must have rigorous structure, clear layers, physical logic, persistent energy arcs, and real interaction with environment.
- Build from inside to outside: mechanical skeleton -> transmission structure -> armor plates -> energy / weapon activation.
- Use concrete assembly verbs: gears mesh, precision parts interlock, skeleton unfolds, buckles align, plates flip/fold/slide/lock, seams vent steam/sparks/energy arcs.
- Helmet assembly should be staged: neck/back-head parts extend, jaw closes, side parts slide and lock, lower mask folds upward, upper mask folds downward, final seams glow.

One-continuous-shot rules:

- If the user asks for 一镜到底, write `continuous long take / one continuous shot` and state no hard cuts, no jump cuts, no montage, no black-screen transition, no hidden transition.
- Scene scale and shot-size changes must happen through real camera movement: push-in, pull-back, lateral tracking, orbit, follow, crane rise/drop, or reframing.
- For high-speed flight, launch, or charging mobs, include speed, scale, count contrast, compressed crouch/load, ground water/dust/debris disturbance, air tearing, engine flare, motion blur, speed lines, air cone, sonic impact, and wind pressure shaking the camera.

Time-axis recipes:

7-second Seedance structure:

```text
0-1s: establish scene, relationship, subject count, spatial position.
1-3s: push-in or lateral tracking enters dialogue/action preparation.
3-5s: action or emotion escalates.
5-7s: pull-back/lateral move reveals completed body action, transformation, attack, or reversal; then move to half-shot/close-up for final line if needed.
```

15-second VFX/action structure:

```text
0-2s: trigger and local detail.
2-5s: core change or conflict escalation.
5-9s: key subject completes transformation/change.
9-12s: high-speed movement, scale expansion, number contrast.
12-15s: burst, reaction, shockwave, ending state.
```

Sound binding:

- Sound must be bound to action. Use it to confirm contact, scale, material, speed, or silence.
- Examples: rain impact, monster hiss, electric arc while fist clenches, gear mesh, steam jet, metal scrape from sword draw, high-speed air rip, explosion shockwave, ground impact, glass/water/table reflections vibrating.

Visual cleanliness and neutral expression:

- Keep `【画面清洁与限制】` short and targeted to the likely failures: image blur, identity drift, face drift, hairstyle/costume drift, subject count errors, prop appearing from nowhere, spatial confusion, jump cuts, action stutter, low-quality VFX, unnatural dynamic lighting.
- Add specialized avoid rules only when relevant: mecha structure collapse, armor turning liquid, helmet appearing suddenly, wrong finger count, weapon appearing from nowhere, energy arc disappearing; multi-head count drift; exaggerated crying or fake tears.
- Use neutral visual wording when needed: `尸体` -> `倒地的人物`; `死亡` -> `被击倒 / 失去战斗能力`; `血腥` -> `冲击痕迹 / 战斗痕迹 / 烟尘`; `残肢` -> `破碎护甲 / 飞散碎片`; `杀死` -> `击倒`.

## 0B. Silent Decision Engines

Use these engines silently before writing any visible prompt for complex scripts, accidents, action scenes, emotional close-ups, multi-shot sequences, reference-frame reconstruction, or model-repair work. Do not expose these engines unless the user asks for analysis. Their output must appear indirectly through better shot choices, clearer camera language, stronger causality, and more executable Seedance segments.

Source-informed basis:

- CineTechBench treats cinematographic technique as analyzable across shot scale, shot angle, composition, camera movement, lighting, color, and focal length.
- Intelligent cinematography research separates pre-production shot planning, production camera control, virtual production, live production, and aerial production; use that as a reminder to distinguish planning, camera behavior, and model execution.
- OpenTimelineIO models editorial work as timelines with clips, timing, tracks, transitions, markers, and metadata; use this to think in units, transitions, hooks, and timeline state.
- Classical film grammar terms such as POV, reaction shot, off-screen space, continuity editing, the 180-degree rule, eyeline match, and match on action are spatial logic tools, not decoration.
- Cutting/DeLong/Nothelfer research on changing Hollywood form reinforces that duration, motion level, darkness/contrast, and attention rhythm interact; short shots should carry high-motion or single-impact information, while long shots need internal visual change.
- ACES-style color thinking prioritizes consistent creative intent, camera matching, and removal of ambiguity in color communication.
- Stable virtual camera research highlights camera trajectories such as orbit, spiral, zoom-out, dolly zoom-out, and the need for viewpoint consistency.
- Video/audio benchmarks such as MovieGenBench evaluate human activity, physics, motion level, ambient sound, and sound effects; prompts should therefore bind motion, physics, and sound explicitly.

### Director Intent Engine

Purpose: determine why the scene exists before deciding how it is shot.

Silent questions:

```text
DRAMATIC QUESTION: What question should the audience be waiting to answer?
VIEWPOINT OWNER: Whose knowledge, fear, desire, or mistake guides this shot?
INFORMATION ORDER: What must be hidden, hinted, revealed, then confirmed?
EMOTIONAL CURVE: What changes from start to end: calm -> pressure, doubt -> proof, confidence -> fear?
SHOT PURPOSE: Is the shot establishing geography, revealing information, confirming action, showing reaction, or changing scale?
PROMPT CONSEQUENCE: Which visible action, camera movement, light change, sound cue, and ending state express that purpose?
```

Rules:

- If there is no new information, emotional shift, viewpoint shift, scale shift, or action result, do not add a shot.
- When danger matters, show the safe assumption first, then the hidden hazard, then the irreversible action path.
- When emotion matters, decide whether the audience should know more than the character, less than the character, or learn with the character.
- When comedy matters, play the action seriously; make the mismatch, delay, or reaction carry the joke.
- When a scene is instructional or safety-oriented, prioritize readable causality over spectacle.
- Convert abstract themes into visible choices: distance, blocked route, object placement, eye line, hesitation, hand movement, sound drop, or light shift.

Prompt kernel:

```text
DIRECTOR INTENT: This shot exists to [establish / reveal / withhold / confirm / escalate / reverse] [specific story information] from [viewpoint owner]'s perspective.
```

### Scene Function Router v2

Purpose: when the user gives only a feeling, rough scene, famous-scene reference, or short premise, choose the scene function first. This router is silent; it selects the narrative mechanism that later drives geometry, camera, performance, editing, sound, and Seedance compression.

Rules:

- Do not start from a camera move. Start from what changes: information, power, danger, scale, relationship, time, emotion, or consequence.
- A scene may combine two functions, but one must be primary. Example: `confession + threat entrance`, `chase + crowd escape`, `disaster warning + aftermath`.
- The selected route must become concrete inside `【运镜与时间轴】`: screen-left/right, foreground/midground/background, focus path, body mechanics, sound cue, cut reason, and ending state.
- If the route requires more than 15 seconds, split at the natural state change: setup/reveal, route/contact, decision/consequence, transformation/final form.

| Scene function | User trigger | Silent structure to compile |
|---|---|---|
| Power dialogue | 谈判、威胁、饭桌、审问、对峙 | establish axis -> OTS/reverse -> reaction owner -> evidence/object insert -> power shift by angle, distance, height, or silence |
| Confession / lie | 告白、隐瞒、撒谎、真相 | stable two-shot -> face mask -> hand/breath leak -> object/eye insert -> listener reaction -> space widens or closes |
| Investigation | 查案、盘问、发现线索 | neutral geography -> clue insert -> POV or eyeline check -> reaction cut -> procedural hand action -> new question |
| Overheard secret | 偷听、隔墙、门外、意外听见 | foreground barrier -> muffled off-screen sound -> partial ear/hand/body -> forbidden information -> escape or interruption risk |
| Suspense search | 找人、夜路、走廊、失踪、恐怖 | sound first -> POV scan -> empty frame hold -> edge movement -> snap focus or occlusion reveal |
| Threat entrance | 反派登场、危险靠近、陌生人出现 | environment reacts first -> feet/hand/shadow -> victim reaction -> partial face -> full posture with exit blocked |
| Chase / escape route | 追逐、逃跑、路线被堵 | route map shot -> low follow or lateral track -> obstacle -> body solution -> pursuer counteraction -> narrowing exit |
| Crowd escape | 人群、市场、踩踏、混乱 | main flow -> counterflow -> congestion point -> protagonist against flow -> blocked route -> new route reveal |
| Rescue / sacrifice | 救援、坠落、抢救、来不及 | danger line -> failed grip/force point -> rescuer route -> strain insert -> success/failure consequence |
| Fight exchange | 打斗、搏斗、格挡、反击 | stance/distance -> attack vector -> contact/block -> recoil -> counterforce -> decisive result -> aftermath |
| Disaster warning | 事故、灾难、机器、坍塌 | normal routine -> anomaly insert -> ignored warning -> hazard path -> reaction delay -> irreversible contact/result |
| Scale awe | 神迹、巨物、宇宙、沙漠 | tiny human reference -> environmental scale -> slow reveal -> low-frequency sound -> human reaction after reveal |
| Social pressure | 羞辱、围观、被审判、公众压力 | crowd as witness -> protagonist isolated by frame -> reaction chain -> public object/line -> silence or verdict |
| Memory / longing | 回忆、遗憾、错过、想念 | present tactile object -> matched gesture -> alternate space/color -> return to present with changed face/body |
| Temptation / desire | 欲望、选择、三角关系 | base action -> two competing color/object anchors -> repeated glance/action -> proportion shows inner weight |
| Montage task pressure | 训练、工作、重复、赶时间 | normal action -> repeated variants -> complication -> acceleration -> callback to first action with changed state |
| Transformation / resolve | 觉醒、变身、重生、下定决心 | defeated state -> inner trigger -> body/eye/focus change -> environment reaction -> test hit -> final silhouette |
| Comedy delay | 尴尬、反差、荒诞 | serious setup -> tiny wrong detail -> delayed look -> stillness -> reaction owner -> consequence without overacting |
| Product / craft process | 产品、拉花、手作、科普 | material close-up -> hand/tool path -> process state change -> texture confirmation -> final clean hero state |
| Sports / broadcast | 比赛、直播、进球、赛事 | crowd reaction -> field play tracking -> impact slow insert -> scoreboard/crowd return -> celebration or disbelief |
| Vehicle danger | 赛车、追车、倒车、撞击、农机 | driver/hand/road setup -> vehicle vector -> blind spot/hazard -> low wheel/road or machine insert -> impact/evasion/result |
| Long-take route | 一镜到底、走廊、空间调度 | empty start frame -> actor enter -> internal marker beats -> occlusion/turning point -> exit or settled ending |
| Reversal reveal | 反转、身份暴露、真相翻盘 | false frame premise -> withheld clue -> reaction before fact -> reveal detail -> wider consequence shot |
| Aftermath / verdict | 结尾、结果、沉默、后果 | hold on consequence object/body/space -> sound decays -> witness reaction -> final fixed frame |

Prompt kernel:

```text
SCENE FUNCTION ROUTE: primary route [function], secondary route [optional]; story change is [information/power/danger/scale/relationship/consequence]; compile through [structure beats] and end on [new state].
```

### Scene Geometry & Axis Engine

Purpose: make the viewer understand where everyone and everything is, especially before action, accidents, pursuit, crowds, or dialogue.

Silent map:

```text
SPACE: room / road / greenhouse / battlefield / market / vehicle / table.
AXIS OF ACTION: line between character-character, character-object, character-threat, or movement direction.
CAMERA SIDE: stay on one side of the 180-degree axis unless disorientation is intentional.
SCREEN DIRECTION: left-to-right, right-to-left, toward camera, away from camera.
ENTRANCES / EXITS: where bodies can enter, escape, or be trapped.
DANGER LINE: object or route that becomes unsafe if crossed.
FOREGROUND / MIDGROUND / BACKGROUND JOBS: each depth layer must carry a task.
OFF-SCREEN SPACE: sound, gaze, shadow, or reaction can imply what the frame does not show.
```

Rules:

- Establish the geography before contact-heavy action or irreversible danger.
- Preserve screen direction across shots. If the axis changes, reset with an establishing shot, overhead, neutral frontal angle, or clear camera move.
- Use eyeline match when a character sees a clue: face looking -> object seen -> reaction.
- Use POV only when the audience must share limited knowledge or panic; otherwise prefer objective geography.
- Use reaction shot when the event's meaning is more important than the event itself.
- Use match on action when continuity matters across a cut: the same movement bridges two shots.
- Give foreground, midground, and background separate jobs. Example: foreground pipe, midground operator, background exit.
- For accidents and safety scenes, name the fixed hazard, moving body, narrowing gap, blocked route, and final state without sensationalizing injury.

Prompt kernel:

```text
GEOMETRY LOCK: camera stays on the [left/right/front] side of the action axis; [subject] moves [screen direction]; [hazard/goal] remains fixed in [foreground/midground/background]; entrance is [position], exit is [position], danger line is [object/route].
```

### Frame Composition & Visual Parsing Engine

Purpose: convert scene geography into a concrete image that Seedance and other video models can parse. This engine does not replace the camera/lens and lighting choice, and it does not require a standalone output section by default. First lock the segment-level `【基础风格】` with camera/lens and lighting/color, then feed the readable frame structure, focus path, and ending state into `【运镜与时间轴】`.

Seedance priority:

- Seedance often follows visible frame structure more reliably than abstract directing language.
- Write what is visible before what it means: left/right, foreground/background, focus, blocking, fixed object, moving subject, and composition.
- Use English locks when Chinese can blur camera/action meaning: `screen-left`, `screen-right`, `foreground`, `midground`, `background`, `rack focus`, `frame edge`, `centered composition`, `diagonal composition`.

Silent frame ledger:

```text
FRAME ORIENTATION: horizontal / vertical / square / wide-screen, camera side.
SCREEN LEFT:
SCREEN RIGHT:
CENTER:
UPPER FRAME:
LOWER FRAME:
FOREGROUND:
MIDGROUND:
BACKGROUND:
FRAME EDGES:
DEPTH / OCCLUSION:
FIXED OBJECTS:
MOVING SUBJECTS:
FOCUS START:
FOCUS TRANSFER:
FOCUS END:
ENTRY / EXIT:
COMPOSITION:
```

Composition choices:

| Composition | Use when | Prompt wording |
|---|---|---|
| centered composition | action readability, comedy, impact, symmetrical threat | `centered composition, main subject locked in frame center` |
| rule of thirds | natural drama, interview-like realism, directional gaze | `subject on left third, empty right side shows the route` |
| symmetrical composition | ritual, institution, inevitability, cold order | `symmetrical frame, corridor lines converge behind the subject` |
| diagonal composition | chase, fall, danger line, spatial pressure | `diagonal composition from foreground-left hazard to background-right escape path` |
| leading lines | routes, roads, greenhouse rows, tunnels, crowd flow | `greenhouse metal pipes create leading lines toward the rear hazard` |
| frame-within-frame | entrapment, surveillance, doorway/window reveal | `subject framed inside the narrow doorway, pipe edge cutting the foreground` |
| over-the-shoulder | dialogue, inspection, clue ownership | `OTS over the worker's shoulder toward the fixed pipe` |
| top-down map | clarify routes, crowd flow, accident geometry | `top-down 90-degree view showing tractor, pipe, exit route, and danger gap` |
| low-angle foreground dominance | machinery, monster, vehicle, authority | `low-angle foreground machine handle dominates the lower frame` |
| negative space | isolation, unseen threat, dread, off-screen sound | `large empty screen-right space, threat sound comes from off-screen right` |

Rules:

- Put frame structure before abstract style in model-facing prompts.
- Screen-left/right and foreground/background are hard constraints for model parsing, not optional decoration.
- If a subject enters, name entry side, depth plane, travel direction, destination, and blocking object.
- If a subject exits, name the edge or route and what remains after exit.
- If focus changes, name the start subject and end subject: `rack focus from foreground hand gripping the handle to background fixed metal pipe`.
- If an object is dangerous, separate fixed and moving elements: fixed pipe in background, moving handle in foreground, narrowing gap between them.
- For safety/accident material, avoid graphic spectacle; make causality readable through geometry, pressure, blocked route, and sound.
- Do not write only "cinematic composition", "镜头推进", "压迫感", or "高级构图"; translate them into frame layout and focus behavior.
- In default Seedance output, do not create separate `【画面结构与构图】`, `【焦点路径】`, or `【结尾状态】` sections. Fold them into `【运镜与时间轴】`.
- If the user asks for no timeline or no time-axis output, then provide standalone `【画面结构与构图】`, `【焦点路径】`, and `【结尾状态】` sections so the structural decisions remain visible.

Prompt kernels:

```text
FRAME STRUCTURE: screen-left [object/action], screen-right [object/action], center [main subject], foreground [object], midground [subject], background [hazard/route].
COMPOSITION: [centered/rule of thirds/diagonal/leading lines/frame-within-frame], chosen to make [danger/route/emotion/scale] readable.
FOCUS PATH: focus starts on [subject/object], rack focus to [second subject/object], ends on [final story information].
ENTRY PATH: [subject] enters from frame-left foreground, moves diagonally toward midground center, while [fixed object] remains in background-right.
OCCLUSION: [foreground object/person/smoke/door frame] briefly crosses the lens and motivates the transition.
```

### Body-Part Action Decomposition Engine

Purpose: turn generic verbs into visible mechanics so the model can animate body motion instead of guessing a result.

Silent body ledger:

```text
HEAD / EYES:
SHOULDERS:
ELBOWS:
WRISTS / HANDS:
TORSO:
WAIST / HIPS:
KNEES:
FEET:
WEIGHT SHIFT:
PROP CONTACT:
ENVIRONMENT CONTACT:
FORCE SOURCE:
FAILURE POINT:
RECOIL:
RECOVERY POSE:
SOUND CONFIRMATION:
```

Rules:

- Replace "挣扎", "逃跑", "攻击", "转身", "摔倒", "后退", "救援" with a body path.
- Start with the body part that initiates motion, then state force transfer, object contact, visible result, and recovery.
- For a turn: eyes/head lead, shoulders rotate, torso follows, feet or hips replant, prop/handle reacts.
- For backing up: head checks direction, shoulders twist, hands maintain grip, one foot steps back, weight shifts, object moves, fixed hazard stays visible.
- For a fall: foot slips or support fails, knee buckles, hip drops, hand reaches, contact sound confirms impact, body settles into a recovery pose.
- For a strike/grab/rescue: force source -> limb path -> contact point -> target reaction -> recoil/recovery -> sound confirmation.
- For a conflict exchange: attacker route -> defender counter-route -> evade/block/contact -> counterforce -> escalation or charge -> decisive contact -> aftermath consequence.
- For accidents and safety scenes, keep the description neutral and procedural; the body mechanics clarify causality without graphic injury detail.

Prompt kernels:

```text
BODY ACTION PATH: head turns over left shoulder; right hand tightens on the handle; left foot slides backward; body weight shifts to the rear heel; the handle moves toward the fixed pipe.
CONTACT MECHANICS: [limb/prop] contacts [object/body point], force comes from [body/vehicle/machine], [object/body] reacts by [visible result], sound is [specific material cue].
RECOVERY STATE: body ends [standing/crouched/fallen/off-balance], hands [still gripping/released], gaze [fixed on hazard/away/blank], motion [continues/stops].
```

### Action Exchange & Escalation Engine

Purpose: convert game-boss prompt structure into live-action film action grammar without copying game nouns. The reusable value is not lightning, boss names, UI, or loot. The reusable value is the rhythm of route, contact, counterattack, charge-up, decisive impact, and aftermath.

Core exchange grammar:

```text
ARENA LOCK: where the fight happens, screen direction, distance, obstacles, exits, danger line.
ROUTE: attacker/actor moves from [start] through [path] toward [target].
FIRST THREAT: opponent, machine, vehicle, crowd, or environment sends a visible counterforce.
EVASION / BLOCK / CONTACT: body or prop solves the threat with a readable movement.
CONTACT POINT: exact body part, prop edge, grip point, surface, joint, or obstacle hit.
COUNTERFORCE: opponent or environment reacts; action is not one-sided.
ESCALATION: second attack, new route, blocked exit, stronger force, reduced distance, or higher risk.
CHARGE-UP: breath, stance, grip, foot plant, prop lift, light/sound/environment change before climax.
DECISIVE CONTACT: final hit, grab, rescue, reveal, door break, machine stop, fall, or escape.
AFTERMATH: silence, stillness, debris, dropped object, changed posture, unlocked route, or visible consequence.
```

Game-to-live-action conversion:

| Game prompt element | Reusable action logic | Live-action translation |
|---|---|---|
| lightning sword / energy trail | visible force path | body momentum, blade/prop arc, flashlight beam, dust trail, wet floor reflection, cloth snap |
| BOSS sweep / bite / stomp | opponent counterforce | punch, shove, vehicle swing, machine arm, falling beam, crowd surge, animal charge |
| hit sparks / VFX burst | contact confirmation | material sound, dust puff, metal scrape, glass crack, shoulder recoil, breath impact |
| skill charge / ultimate | climax preparation | foot plant, two-hand grip, breath hold, silence drop, light flicker, muscles tense, prop raised |
| health bar clear | objective result | opponent drops weapon, machine shuts off, door opens, alarm stops, crowd freezes, victim reaches safety |
| loot drop | consequence tableau | keys, phone, weapon, documents, tools, medicine, badge, broken part, witness evidence, empty space after threat |
| UI fade | non-diegetic layer removal | remove overlays; return to physical world, room tone, silence, and grounded aftermath |

Action exchange ladder:

```text
1. Establish arena and distance.
2. Threat displays power through environment before direct contact.
3. Protagonist begins a route with visible footwork and body orientation.
4. Opponent counters; the route is interrupted.
5. Protagonist evades, blocks, or redirects force.
6. Contact point lands; environment and sound confirm it.
7. Opponent reacts and creates a stronger counterforce.
8. Protagonist charges a decisive action through stance, grip, breath, and silence/light/sound change.
9. Decisive contact changes the scene state.
10. Aftermath holds long enough to show consequence.
```

Rules:

- Do not let attack trails replace physical contact. Write both the visible trail/path and the body/prop contact point.
- Do not make the opponent passive. Every major attack should create a counterforce, interruption, block, miss, recoil, or changed route.
- Do not jump from normal fight to climax. Add charge-up: stance lowers, grip tightens, breath holds, camera steadies, sound narrows, environment responds.
- Consequence is required. After the decisive moment, show what remains: stillness, debris, dropped prop, changed body posture, stopped machine, open exit, silent room, or witnesses reacting.
- For live action, reduce game VFX density. Use practical material feedback: dust, sweat, fabric, metal, glass, concrete, water, breath, room tone, and silence.
- For Seedance, keep each action exchange to one readable chain per beat. If there are three attacks and two counters, assign time windows.

Prompt kernels:

```text
ACTION EXCHANGE: [subject A] moves from [start] toward [target] along [route]; [subject B/hazard] counters with [counter-route/force]; [A] evades/blocks/contacts using [body part/prop]; contact point is [exact point]; result is [visible change]; sound confirms with [material cue].
CHARGE-UP: [feet/stance/grip/breath/eyes] lock into preparation; [environment/sound/light] changes; camera holds for [duration] so the decisive action feels earned.
AFTERMATH CONSEQUENCE: after contact, [threat/object/body/space] ends in [new state]; [sound] drops to [silence/room tone/low hum]; [prop/evidence/route] remains visible for the next beat.
```

### Plot Reversal & Visual Impact Engine v3

Purpose: when the user asks for "more cinematic", "stronger impact", "a twist", "more like a famous movie feeling", or "make it shocking", choose a story-changing reveal mechanism instead of adding empty spectacle.

Reversal rule: spectacle is only valid when it changes audience knowledge, character knowledge, conflict state, power, danger, scale, or consequence.

| Reversal / impact type | Story change | Camera / edit mechanism | Prompt kernel |
|---|---|---|---|
| danger line reveal | safe space becomes hazard | foreground/midground/background relation, rack focus, top-down or pull-back | `danger line reveal: focus shifts from the unaware subject to the hidden hazard line behind/under/beside them` |
| object value flip | ordinary prop becomes evidence, weapon, memory, trap, or proof | insert -> reaction -> wider relation | `object value flip: ordinary [object] becomes [evidence/threat] when [sound/light/touch] reveals its function` |
| safe space turns hostile | home, car, table, bed, elevator, field, or office becomes a trap | locked-off normality breaks, threshold closes | `safe space reversal: the familiar room stays still while [door/window/machine/crowd] changes state into danger` |
| off-screen cause / on-screen effect | unseen force becomes larger than the frame | sound-first cue, reaction cut, environmental effect | `off-screen threat: sound arrives first, visible objects react, character turns before the source is revealed` |
| false victory | success becomes a worse problem | hold half beat after success, reveal consequence | `false victory: action seems complete, camera holds, then background/prop/body reveals the cost` |
| delayed consequence | impact lands after a small silence | contact -> stillness -> result | `delayed consequence: contact happens, sound drops, body/space reacts half a beat later` |
| scale inversion | private problem becomes disaster scale | pull-back, crane rise, EWS, crowd reference | `scale inversion: camera pulls back from personal detail to reveal the full disaster geometry` |
| power swap | passive side gains control | camera height, seated/standing relation, door/table/stair blocking flips | `power swap: the lower/blocked character controls [object/exit/evidence/silence], reframing the power relation` |
| information asymmetry | audience, protagonist, and opponent know different facts | cross-cut, eyeline, background clue, reaction owner | `information asymmetry: audience sees [hidden fact] while the character continues toward [wrong action]` |
| moral reversal | victory reads as loss, loss reveals truth | reaction holds longer than action result | `moral reversal: the event appears successful, but the reaction owner's silence changes its meaning` |

Rules:

- Always define initial assumption, hidden fact, reveal mechanism, reaction owner, and new ending state.
- Use sound-first reveals for threats that should feel larger than the frame.
- Use rack focus when power or information moves from one subject/object to another.
- Use pull-back scale reveal or crane rise when the audience needs to learn that the scene is bigger, worse, or more isolated than expected.
- Use delayed consequence when physical impact should feel heavier: contact -> brief stillness -> result/sound/body response.
- For accident/safety material, use visual reversal to reveal danger lines and blind spots, not to sensationalize injury.

Prompt kernel:

```text
VISUAL REVERSAL: audience first follows [safe assumption]; camera/focus/sound reveals [hidden fact]; [reaction owner] registers it through [face/breath/body]; ending state changes to [new danger/power/scale/consequence].
```

### Famous Scene Feeling Compiler v3

Purpose: understand the user's film/anime/animation "feeling" and translate it into original cinematic grammar. This is a silent compiler, not a trivia module and not a replication instruction.

Copyright and reference boundary:

- Use film titles only as internal trigger labels when the user uses them.
- Output original characters, location, props, dialogue, wardrobe, and blocking unless the user owns/provides authorized references and explicitly asks for direct reconstruction.
- Do not reproduce protected lines, exact shot order, exact staging, character likeness, costume, set dressing, or franchise identifiers by default.
- Translate the request into spatial pressure, power geometry, movement semantics, performance layers, light, sound, edit rhythm, and story-state change.

Reusable mechanism cards:

| User feeling / reference family | Reusable mechanism | Prompt kernel |
|---|---|---|
| broken-door dread / threshold horror | safety boundary is attacked; barrier state changes; inside subject loses options | `threshold horror: [door/window/curtain/elevator/vehicle] is the danger line, repeated impacts change its state, interior subject retreats, breath catches, material sound marks escalation, final crack reveals only a partial threat` |
| shadow authority / crime power | low-key practical light, still seated body, lower supplicant, long silence | `shadow authority: low-key practical light hides the eyes, still seated figure controls the room, foreground supplicant leans lower, silence and hand movement carry threat` |
| bullet-time / time-slice decision | decisive instant stretches; camera orbits suspended action; particles prove slowed time | `time-slice decision: action freezes at the decision/contact point, camera orbits suspended body/object, dust/fabric/debris hang in air, sound narrows to a low pulse, then time snaps back to consequence` |
| epic action tableau | lateral route, readable silhouette, speed ramp, contact/recoil/consequence | `epic action tableau: lateral tracking keeps the action vector clear, speed ramp slows before contact, body silhouette stays readable, impact returns to real speed, dust/recoil confirms the hit` |
| vertigo truth collapse | realization changes space; background stretches/compresses around frozen face | `Hitchcock dolly zoom: camera dollies in while zooming out, background stretches away from the frozen face, breath stops, room tone drops, realization lands before the cut` |
| psychological montage | face, object, consequence, symbol, and sound collision create meaning | `psychological montage: cut between face, object, consequence, and symbolic detail; each shot adds one meaning unit; sound bridges the fragments; final shot resolves the idea` |
| corridor fate / long-take entrapment | long axis, narrowing walls, off-screen pull, escape route shrinks | `corridor compression: centered subject moves down a long axis, walls converge, off-screen sound pulls them forward, exit behind shrinks with each step` |
| table battlefield | table/desk becomes war line; hands and objects become weapons | `table battlefield: table edge splits opponents, foreground hands control objects, eyelines cross over the surface, silence holds before the decisive gesture` |
| surveillance uncertainty | incomplete evidence, obstructed POV, off-screen cause, delayed reaction | `surveillance uncertainty: restricted viewpoint sees only fragments, sound implies unseen action, reaction arrives before full proof` |
| long-take entrapment | no cut escape; internal beats trap audience with character | `oner entrapment: one continuous shot crosses [beat 1/2/3], camera cannot escape the room/vehicle/street, each new obstacle closes another route` |
| memory match cut | present and memory linked by shared shape, gesture, color, or sound | `memory match cut: [hand/door/light/sound] in the present matches [past/fantasy image], cutting across time while preserving emotional continuity` |
| scale awe / disaster reveal | tiny human reference, immense negative space, slow camera, low-frequency sound | `scale awe: tiny human silhouette anchors the frame, camera pulls back or cranes up to reveal overwhelming space, low-frequency sound marks mass` |
| animation impact / sakuga hit | anticipation -> path -> contact -> smear/impact frame -> recoil -> recovery | `animation impact grammar: body lowers into anticipation, motion path is readable, contact lands on one clear point, impact frame holds briefly, recoil and recovery show consequence` |
| quiet emotional collapse | emotion leaks through breath, hand, shoulders, and delayed blink instead of big gesture | `quiet collapse: face stays controlled, breath breaks, hand loses grip, shoulders drop, silence carries the emotional turn` |
| false-calm dread | calm composition hides background/off-screen threat | `false-calm dread: locked-off calm frame holds too long, background detail or off-screen sound changes first, subject remains unaware` |
| leap-of-faith growth | camera orientation or fall direction reframes danger as transformation | `leap-of-faith: subject falls or steps into empty space, camera orientation reframes falling as rising, sound opens from breath to wide atmosphere` |

Prompt compiler rule:

```text
FAMOUS-SCENE FEELING TRANSLATION: user reference [film/anime/scene feeling] -> original mechanism [threshold / shadow authority / time-slice / epic tableau / vertigo truth / montage collision / long-take entrapment / scale awe / animation impact]; preserve no protected names, dialogue, costumes, exact staging, or franchise identifiers.
```

### Montage & Time-Distortion Compiler

Purpose: convert "montage", "flashback feeling", "psychological impact", "anime speed", or "time distortion" into explicit time-axis instructions.

| Montage type | Use when | Construction rule |
|---|---|---|
| metric montage | countdown, machine process, training, ritual | cut by fixed beat length; each insert changes one information unit |
| rhythmic montage | chase, labor, fight, crowd flow | cut by movement direction, collision, footstep, door slam, or object path |
| tonal montage | grief, longing, dread, memory | cut by emotional temperature, color, sound texture, and actor breath |
| overtonal montage | climax pressure | action rhythm + emotion + sound + color intensify together |
| intellectual montage | abstract meaning | two unrelated images collide to create a third idea |
| psychic echo cut | fate, trauma, supernatural link | present action cuts to matching gesture/object/sound in another time or mind |
| memory match cut | intimate memory | same shape, hand motion, doorway, flame, rain, vehicle light, or sound bridges time |
| speed-ramp insert | action impact | normal speed anticipation -> slow contact -> fast consequence -> held aftermath |

Rules:

- Each insert must change time, place, emotion, evidence, pressure, or consequence.
- Do not write "fast montage" alone. Name the connective tissue: visual rhyme, sound bridge, action match, color match, object match, or rhythm match.
- End every montage with a new story state, not just atmosphere.

Prompt kernel:

```text
MONTAGE COMPILER: each insert changes [time/place/emotion/evidence/pressure]; connect shots by [visual rhyme/sound bridge/action match/color match]; final image lands on [new story state].
```

### Genre Scene Grammar Packs

Purpose: when the user says a broad feeling, silently choose the correct mechanism family before writing prompts.

| Genre feeling | Mechanism pack | Prompt priorities |
|---|---|---|
| horror threshold | door, window, mirror, curtain, hallway, bed edge, basement, off-screen sound | danger line, partial reveal, sound-first threat, stillness after impact |
| crime power | table, chair height, shadow, hands, object exchange, silence | low-key practical light, stillness, object control, reaction ownership |
| action route | chase path, obstacle, counterforce, contact, recoil, recovery | route clarity, screen direction, contact point, consequence sound |
| disaster scale | tiny human, crowd route, blocked exit, top-down geometry, low-frequency mass | scale inversion, crowd flow, delayed consequence, aftermath state |
| sci-fi perception | interface, reflection, vacuum, body anomaly, subjective time | rule reveal, time-slice, sound narrowing, material reaction |
| romance memory | repeated gesture, reflected surface, color anchor, missed eyeline, unspoken pause | memory match cut, quiet performance leak, soft motivated light |
| animation impact | anticipation, smear/impact frame, held contact, elastic recoil | readable path, single contact point, expressive timing, clean silhouette |
| absurd comedy | serious action, wrong result, delayed reaction, object failure | timing reversal, deadpan face + body chaos, clean result frame |

### Cinematography Decision Engine

Purpose: choose shot scale, angle, composition, movement, focal length feel, and camera state because they serve story function.

Decision matrix:

| Story function | Shot / lens choice | Camera behavior | Prompt effect |
|---|---|---|---|
| Establish geography | WS/EWS, 24-35mm feel, level camera | locked-off or slow lateral move | readable exits, obstacles, routes |
| Reveal hidden danger | CU/insert to MS/WS relation, 35-50mm feel | rack focus or slow push-in | object becomes narrative threat |
| Isolate emotion | CU/MCU, 50-85mm feel | slow dolly in or locked-off stillness | face and breath become primary action |
| Show body mechanics | MS/MLS, 28-50mm feel | lateral tracking or stable follow | limbs, weight, prop path readable |
| Show scale | WS/EWS, 18-35mm or large-format feel | pull-back scale reveal / crane rise | human-to-world ratio clear |
| Compress pursuit / surveillance | telephoto feel, long-lens compression | lateral or fixed observation | distance collapses, pressure increases |
| Subjective panic | 24-35mm feel, closer distance | handheld documentary camera | imperfect frame, urgent body sound |
| Procedural tension | 35-65mm feel, centered or symmetrical | locked-off precision | cold observation, object evidence |

Rules:

- State shot scale, camera height, camera distance, focal feel, movement, and why the frame changes.
- Wide focal feel exaggerates proximity, space, speed, and edge distortion; use it for panic, cramped interiors, fast foreground motion, or spatial immersion.
- Normal focal feel preserves human proportion and geography; use it for natural drama and instructional clarity.
- Telephoto focal feel compresses depth, isolates faces, flattens crowds, and makes pursuit feel closer; use it for surveillance, emotional isolation, or distant threat.
- Low angle increases power, threat, monumentality, or machinery dominance; high angle reduces control, clarifies layout, or shows vulnerability.
- Handheld is not just shake: it means reactive framing, imperfect timing, and human presence.
- Locked-off is not boring: it means evidence, inevitability, precision, or institutional coldness.
- Stabilized movement means the camera has intent; choose it when the viewer must follow action rather than feel panic.
- If using orbit, spiral, zoom-out, or dolly zoom-out, state the story reason: reveal scale, trap the character, show transformation, or express realization.

Prompt kernel:

```text
CAMERA DECISION: [shot scale], [camera height], [distance], [focal length feel], [movement], chosen to [establish / isolate / reveal / compress / disorient / confirm] [story function].
```

### Lighting Motivation Engine

Purpose: make light feel like it comes from the world while still controlling emotion and readability.

Silent lighting plan:

```text
SOURCE: sun, window, practical lamp, candle, neon sign, fire, monitor, moon, fluorescent tube, vehicle headlight, explosion.
DIRECTION: front / side / back / top / low / motivated from frame-left/right.
INTENSITY: soft low, hard high, flickering, pulsing, overexposed edge, dim practical.
CONTRAST: low-key, high-key, high contrast, flat documentary, negative fill.
SHADOW: soft wrap, hard cut, moving flame shadow, deep blocked shadow.
MATERIAL REACTION: skin, metal, glass, water, dust, smoke, cloth, plastic, mud.
COLOR INTENT: preserve palette, separate planes, signal danger, preserve identity.
```

Rules:

- Every light should have a motivated source unless the user asks for stylized abstraction.
- Practical light is visible or implied inside the scene; use it to justify direction and color.
- Negative fill deepens the unlit side of a face or object; use it for pressure, secrecy, or shape.
- Rim/back light separates the subject from dark background; use it for rain, smoke, night, machines, or silhouettes.
- Hard light creates danger, noon heat, evidence, or institutional severity; soft light creates intimacy, realism, or melancholy.
- For safety/accident scenes, use light to clarify hazards: metal edge highlight, shadow gap, reflective pipe, narrowing clearance.
- For AI models, describe material reaction more than abstract mood: wet ground reflects neon; dust reveals sun shafts; glass doubles the danger line.
- Keep color consistent through camera matching and palette locks; write the intended look, not just "cinematic LUT".

Prompt kernel:

```text
LIGHTING MOTIVATION: [source] from [direction] at [intensity], creating [shadow behavior]; [materials] react with [reflection/texture/color], preserving [palette/identity/story clarity].
```

### Editorial Rhythm Engine

Purpose: decide shot order, cut reason, duration, transition, and Seedance compression before writing prompts, then pass duration-sensitive details into the Shot Duration & Timeline Beat Engine.

Timeline logic:

```text
CLIP UNIT: one shot = one primary information unit.
TRACK OF ATTENTION: what the viewer follows: face, object, route, danger, sound, or reaction.
MARKER: key moment inside the shot: reveal, contact, realization, impact, line, silence.
TRANSITION: hard cut, reaction cut, match cut, match on action, sound bridge, J-cut, L-cut, foreground occlusion.
DURATION RATIONALE: why the shot lasts this long: impact, scan, dialogue, posture, atmosphere, immersion, or emotional release.
ENDING STATE: exact visual/sound state that lets the next segment begin independently.
```

Rules:

- Use hard cut when the next shot adds new information or confirms an action result.
- Use reaction cut when audience meaning depends on what a character understands.
- Use match on action when one physical movement crosses a cut and continuity must feel smooth.
- Use match cut when a shape, gesture, color, or sound connects two ideas.
- Use J-cut when sound from the next shot should arrive before the image, creating anticipation.
- Use L-cut when the previous shot's sound should continue over the next image, preserving emotional or spatial continuity.
- Use foreground occlusion when the cut should feel diegetic and model-friendly: passing person, door frame, cloth, vehicle, smoke.
- Use practical duration buckets as defaults, not as law. Duration must follow shot function, information density, motion intensity, emotional hold, sound bridge, and model limits.
- For Seedance, build 15 seconds as 3-6 internal beats, not as many full scenes. Use 6-8 beats only for montage, fight impacts, or rapid parallel information.
- If a shot needs more than one action chain, split it. If the ending state cannot be named, the cut is not ready.

Prompt kernel:

```text
EDIT LOGIC: cut because [information/emotion/viewpoint/conflict/scale/action-result] changes; transition is [type]; duration is [range] because [density/motion/emotion/sound]; ending state is [exact image + sound state].
```

### Shot Duration & Timeline Beat Engine

Purpose: translate a story beat into an executable time axis. Use the image-based cutting table as a practical Seedance baseline, then upgrade it through director/DP logic: what the viewer must read, how much the frame contains, how fast the body/camera moves, how long emotion must stay on screen, and how sound carries or motivates the cut.

Silent inputs:

```text
SHOT FUNCTION: orient / reveal / react / connect / confirm / escalate / breathe / immerse.
INFORMATION DENSITY: one clue / multiple subjects / scene geography / dialogue / action contact / crowd route.
SHOT SCALE: insert / ECU / CU / MCU / MS / MLS / WS / EWS.
MOTION LEVEL: still / micro-expression / gesture / walking / fight / chase / camera move / complex blocking.
CONTINUITY MODE: hard cut / reaction cut / match on action / eyeline match / match cut / sound bridge / J-cut / L-cut / foreground occlusion.
SOUND MARKER: hit, line, breath, silence, low-frequency cue, off-screen warning, sound bridge.
ENDING STATE: exact visual + sound state that makes the next beat readable.
```

Duration ladder:

| Duration | Use when | Director/DP logic | Prompt wording |
|---|---|---|---|
| 0.3-0.7s | subliminal flash, impact insert, panic fragment, memory shard | one object or one body contact only; center the readable action vector | `0.0-0.6s, impact insert, centered composition, metal edge hits frame, sharp metallic impact, hard cut on contact` |
| 0.5-1s | fight contact, chase jolt, shock reaction, quick flashback, fast montage | high motion, low information density; no complex geography | `0.6-1.4s, quick reaction snap, CU, eyes jerk screen-left, breath cuts off, smash cut` |
| 1-2s | daily dialogue beat, continuous action fragment, key clue insert, emotion step | one information unit; viewer needs time to register face/object/action | `1.4-3.0s, key clue, rack focus from foreground hand to background pipe, machine hum rises` |
| 2-3s | multi-person frame, posture relation, scene transition, secondary plot advance | viewer scans body placement and screen direction; useful for axis clarity | `3.0-5.5s, MS two-shot, subject A screen-left, subject B screen-right, eyeline match sets next cut` |
| 3-5s | emotional hold, atmosphere build, important reveal, readable blocking in depth | light, space, and performance need time; let camera or focus change internally | `5.5-9.5s, slow dolly in, foreground obstacle fixed, midground face holds, background danger grows louder` |
| 5-8s | monologue, immersive long take, major atmosphere shot, emotional release/explosion | only works if the shot contains internal reframing, focus shift, body change, or sound change | `9.5-15.0s, one continuous shot, lateral tracking, focus shifts hand -> face -> exit, sound drops to silence` |
| 8-15s | Seedance long take, transformation, complex rescue, scale reveal | use sparingly; must include internal markers every 2-4s so the image does not stall | `0-15s, continuous long take with markers at 3s, 7s, 11s, and final ending state` |

Rules:

- Cut when the audience has received the intended information, not when the seconds feel neat.
- Short cuts work for impact, panic, flash memory, and one clear clue. They are poor for explaining geography, multiple people, or a subtle emotional change.
- More subjects, deeper staging, unclear hazards, or multi-plane composition usually require a longer hold unless the goal is deliberate confusion.
- More camera movement inside one shot usually requires a longer hold; add internal markers so Seedance understands the progression.
- Use match on action when a continuous body movement crosses a cut: preserve step, grip, limb path, weight transfer, contact, recoil, and recovery.
- Use eyeline match when a look motivates the next shot: face looks -> object/hazard appears -> reaction returns.
- Use reaction cuts when meaning depends on understanding, guilt, fear, shock, or relief.
- Dialogue, voiceover, and internal OS require enough time for the line. If the line is too long, split the beat or extend the shot; never cram unreadable speech into a short impact cut.
- A 15s Seedance segment normally contains 3-6 beats. Use 6-8 beats only for montage, fight impacts, or parallel danger. Use 2-3 beats for an immersive long take with strong internal markers.
- `【运镜与时间轴】` should write beats as: `0.0-1.2s | [shot function] | [shot scale/camera] | [frame/focus/action] | [sound marker] | [cut reason/ending state]`.

Seedance timing recipes:

```text
7s standard: 0-1s orientation or clue / 1-3s action setup / 3-5s change, contact, or reveal / 5-7s result and ending state.
10s standard: 0-2s establish axis / 2-4s clue or decision / 4-7s approach, contact, or reveal / 7-10s reaction and hook.
15s safety/drama: 0-2s geography and danger line / 2-4s hidden clue or blind spot / 4-7s decision and body setup / 7-11s approach/contact / 11-13s reaction/result / 13-15s ending state.
15s emotional: 0-3s setup / 3-6s first emotional crack / 6-10s held reaction or body hesitation / 10-13s response / 13-15s hook or unresolved state.
15s action: 0-1.2s impact or route clue / 1.2-2.5s reaction / 2.5-4s contact / 4-6s scale reset / 6-9s chase or struggle / 9-12s result / 12-15s aftermath or hook.
15s long take: 0-4s establish and start movement / 4-8s internal reframing or rack focus / 8-12s core action / 12-15s final state, sound drop, or next hook.
```

Prompt kernels:

```text
TIME BEAT: [start-end], [function], [shot scale], camera [movement], frame [screen-left/screen-right/foreground/midground/background], focus [start -> end], action [body-part path], sound [cue], cut because [reason].
TIMELINE RHYTHM: [fast impact / dialogue continuity / spatial scan / emotional hold / immersive long take], durations chosen because [information density / motion intensity / emotional hold / sound bridge].
```

### Sound Dramaturgy Engine

Purpose: treat sound as story structure, not an afterthought.

Sound layers:

```text
DIEGETIC: sound characters can hear: footsteps, engine, voice, rain, metal, machine, animal, room tone.
NON-DIEGETIC: score, narration, internal OS, stylized sound not heard by characters.
OFF-SCREEN SOUND: sound source outside frame that expands space or warns before reveal.
SUBJECTIVE SOUND: altered hearing from fear, shock, memory, pressure, or focus.
SOUND BRIDGE: sound links shots or enters before the cut.
SILENCE: functional absence of sound; use for shock, realization, vacuum, emotional collapse.
LOW FREQUENCY: scale, disaster, giant mass, machine stress, distant impact.
```

Rules:

- Decide whether each sound is diegetic, non-diegetic, or subjective.
- Use sound first for unseen danger: rumble before collapse, metal creak before failure, animal silence before monster reveal.
- Narrow the sound field when a character realizes something: environment drops, breath or heartbeat remains.
- Cut sound abruptly when action stops, truth lands, or the body loses agency.
- Keep no-BGM requests strict: use现场声、动作声、环境声 only.
- Bind sound to material and force: metal pipe rings, wet mud sucks at boots, glass vibrates, cloth snaps, servo clicks.
- For AI video prompts, sound cues should confirm the visible physics: contact, friction, acceleration, pressure, distance.
- For dialogue, label lip movement vs non-diegetic internal voice. Never let narration accidentally animate the lips.
- When a reference audio controls Seedance rhythm, treat it as a timeline control layer first and a soundtrack second. Mark whether it should be heard in the final output, and bind each major beat to a visible action marker: entry, dash, contact, recoil, reaction cut, camera move, or ending pose.
- If the reference music fights the intended scene function, use only a simplified beat/SFX guide or split the prompt: one version for audio-controlled motion, one version for final clean sound.

Prompt kernel:

```text
SOUND DRAMATURGY: [diegetic/non-diegetic/subjective] sound [leads/confirms/contrasts/cuts off] the action; key cue is [specific sound] tied to [material/force/emotion].
```

### Silent Engine Execution Order

Run these engines in this exact order before the prompt:

```text
1. Director Intent: why this beat exists.
2. Scene Function Router v2: identify the primary scene function and the story state change.
3. Seedance Multimodal Asset Router: assign every @image/@video/@audio a role, dimension lock, and short reusable locked name inside `【角色/场景/素材锁定】`.
4. Scene Geometry & Axis: where bodies, objects, exits, hazards, and camera sides are.
5. Base Style Lock + Visual Style Descriptor: choose project-level camera/lens, color, texture, realism/genre baseline, plus scene-specific lighting/atmosphere changes for `【基础风格】`; repeat this in every independent segment and never write only "same as above".
6. Frame Composition & Visual Parsing: turn geography into screen-left/right, foreground/midground/background, focus path, and composition.
7. Body-Part Action Decomposition: turn generic verbs into visible body-part mechanics and contact paths.
8. Action Exchange & Escalation: for conflict/action, define route, counterforce, contact, charge-up, aftermath, and consequence.
9. Plot Reversal & Visual Impact v3: decide whether the scene needs danger-line reveal, object value flip, false victory, delayed consequence, scale inversion, power swap, or moral reversal.
10. Famous Scene Feeling Compiler v3: if the user asks for a film/anime/scene feeling, translate it into original scene grammar without copying protected details.
11. Actor Emotion & Physical Performance v3: define 目标、阻碍、策略、表面控制、真实泄露、节拍反转、面部、呼吸、身体、手、视线、重心变化和反应归属。
12. Cinematography Decision: refine shot scale, camera height, distance, focal feel, movement, and reveal behavior.
13. Camera Movement Semantics v3: choose movement because it reveals scale, transfers power, discovers danger, clarifies route, preserves action continuity, distorts time, or expresses realization.
14. Montage & Time-Distortion: if the beat needs montage, memory, flashback, speed ramp, or time-slice, define connective tissue and final story state.
15. Genre Scene Grammar Pack: if the user gives a broad feeling, choose horror threshold, crime power, action route, disaster scale, sci-fi perception, romance memory, animation impact, or absurd comedy grammar.
16. Lighting Motivation: refine source, direction, contrast, shadow, and material reaction when the beat needs local lighting detail.
17. Editorial Rhythm: why the shot order and cut type serve information, emotion, viewpoint, conflict, scale, or action-result.
18. Shot Duration & Timeline Beat: choose beat durations by function, density, motion, emotion, sound, and Seedance compression.
19. Sound Dramaturgy + Voice Lock: what sound leads, confirms, narrows, bridges, stops, or preserves character/narrator voice identity.
20. Sequence State & Beat Firewall: for continuation or long projects, record actual accepted opening state, completed beats, current segment job, reserved future beats, and endpoint.
21. Prompt Budget Allocation: choose identity fidelity, motion boldness, or scene density as the primary spend; downgrade or split the rest.
22. Retake / Take Review Protocol: when reviewing a generated take, choose keep, fix in post, edit one layer, re-roll, or rewrite; change only one variable per retake when possible.
23. Model Compiler: compress into Seedance or target-model prompt constraints.
24. Seedance Stability Gate v2: catch drift risks before delivery.
```

Minimal hidden ledger:

```text
INTENT:
VIEWPOINT:
SCENE FUNCTION ROUTE:
SEEDANCE ASSET ROUTER / REFERENCE DIMENSION LOCK:
GEOMETRY / AXIS:
DANGER / REVEAL LINE:
BASE STYLE LOCK / VISUAL STYLE DESCRIPTOR:
FRAME STRUCTURE / COMPOSITION:
FOCUS PATH:
BODY-PART ACTION PATH:
ACTION EXCHANGE / ESCALATION:
VISUAL REVERSAL / IMPACT:
FAMOUS-SCENE FEELING TRANSLATION:
PERFORMANCE INTENT / PUBLIC MASK / PRIVATE LEAK:
CAMERA DECISION:
CAMERA MOVEMENT SEMANTICS:
MONTAGE / TIME DISTORTION:
GENRE SCENE GRAMMAR:
LIGHT MOTIVATION:
EDIT RHYTHM:
SHOT DURATION / TIMELINE BEATS:
SOUND DRAMATURGY:
VOICE / AUDIO LOCK:
SEQUENCE STATE:
BEAT FIREWALL:
PROMPT BUDGET ALLOCATION:
RETAKE / TAKE REVIEW:
SEEDANCE COMPRESSION:
SEEDANCE STABILITY GATE:
```

### Sequence State & Accepted Footage Engine

Purpose: keep long stories from drifting, replaying completed action, or continuing from a planned ending that the model did not actually produce.

Use this engine for continuation, extend, next part, repair-tail, multi-segment stories, generated-take review, and any request that depends on a previous output.

Core rules:

- Plan globally, compile locally: understand the full story and final outcome, but only finalize the current unresolved Seedance segment.
- Accepted footage is canon. If the user accepts a generated clip or final frame, its visible state overrides the written plan.
- Rejected footage is not canon and cannot become the parent of the next prompt.
- If the actual accepted ending is missing, ask for the clip, final frame, or a concrete visible-end description before writing a continuation prompt.
- Scene boundaries are re-anchor points. When the location/time envelope changes, open from canonical references and write an intentional next shot rather than promising seamless continuation.
- Do not chain many output-sourced generations without re-anchoring from original character/scene references; schedule re-anchors before identity drift becomes visible.

Silent state fields:

```text
actual accepted opening state
open motion vector
camera phase
audio phase
completed beats
current segment job
reserved future beats
continuity locks
allowed changes
observed deviation
endpoint
unresolved uncertainty
```

Compiler behavior:

- A previous clip or final frame carries visible state. Text carries the delta: current action, endpoint, missing open-motion/camera/audio phase, and high-risk locks.
- Do not re-describe everything in an attached source. If the prose conflicts with the image/video, the model treats it as drift.
- If a still final frame is attached, infer pose, screen position, wardrobe, props, environment, light, and framing from the still; only ask about what a still cannot show: motion at cut, camera movement phase, or audio phase.

User-facing continuity phrasing should stay Chinese and prompt-ready:

```text
@视频1 是已接受的上一段画面，用作当前段开场状态参考；本段只完成 [当前动作]，不要重复 [已完成动作]，不要提前出现 [未来动作]。从上一段结尾的 [可见状态] 开始，动作方向保持 screen-left -> screen-right，最终停在 [结尾状态]。
```

### Beat Firewall Engine

Purpose: prevent one prompt from performing the whole story at once.

Classify every beat:

| Bucket | Meaning | Prompt behavior |
| --- | --- | --- |
| already happened | previous accepted segment already performed it | do not replay |
| this segment only | current generation may perform it | write in timeline |
| reserved for later | future segment should perform it | do not show yet |
| do not show yet | would spoil, confuse, or overload the current shot | keep out of prompt |

Rules:

- Story context may motivate performance, camera, light, and sound; it must not make the current segment reveal future information, solve later conflict, or skip physical handoff states.
- If accepted footage unexpectedly completes a future beat, mark that beat completed and remove it from future prompts.
- If accepted footage stops short, the next prompt begins from the shortfall instead of pretending the original plan happened.

### Prompt Budget Allocation Engine

Purpose: make Seedance prompts more stable by deciding what the generation is really spending capacity on.

Three competing spends:

| Spend | Buys | Strains |
| --- | --- | --- |
| identity fidelity | stable faces, costume, product shape, logos | bold motion and long chained continuations |
| motion boldness | action, body mechanics, physical impact, choreography | close facial detail, hand precision, product text |
| scene density | crowds, background life, weather, props, large world | individual identity and tiny detail stability |

Method:

1. Choose the primary spend for the segment.
2. Choose at most one secondary spend.
3. Offload fidelity to references when possible.
4. Pay for the primary spend by simplifying the rest: fewer tracked subjects, less face motion, fewer cuts, less text, or a simpler environment.
5. If the prompt needs all three spends at once, split into separate Seedance segments.

Examples:

- Dialogue close-up: primary identity/facial stability, secondary short line; simplify camera, hands, background, and crowd.
- Action beat: primary motion boldness, secondary spatial clarity; express emotion through body posture, not fragile face close-up.
- Crowd/disaster: primary scene density, secondary scale; keep hero large enough in frame and make crowd one directional mass.

### Retake / Take Review Protocol

Purpose: avoid random prompt escalation after a generation returns.

Five verdicts:

| Verdict | Use when | Next move |
| --- | --- | --- |
| keep | primary spend succeeded and flaws are not fatal | accept, log ending state, continue |
| fix in post | flaw is color, trim, sound mix, subtitles, text overlay, or end-frame cleanup | do not regenerate |
| edit one layer | composition/timing are good and only one supported layer is wrong | preserve source and edit that layer |
| re-roll | prompt is good but sample is unlucky | same prompt, new seed or retry |
| rewrite | same flaw repeats across two takes | diagnose mechanism and change prompt |

One-variable rule:

- Change one thing per retake whenever possible: one prompt clause, seed, mode, reference, duration, or camera simplification.
- If several variables change at once, the result cannot teach which fix worked.
- Do not add adjectives to fix systematic failures. Change structure: split beats, simplify motion, re-anchor identity, move text to post, or reduce tracked subjects.

## 1. Product Roadmap Logic

Use the skill as a reusable Film Language Operating System, not a one-off prompt library.

Phase 1 Prompt Library:

- director frameworks
- shot language
- action library
- sound library

Phase 2 Director Knowledge Base:

- director framework library
- cinematographer/camera style library
- style film library
- creature/threat library

Phase 3 Automatic Director System:

- Input: script, novel, image, prompt, or rough idea
- Output: director plan
- Example decisions: use Spielberg Reveal, use Dune Scale, use Mad Max Action

Phase 4 Automatic Storyboard System:

- Output: Shot01, Shot02, Shot03...
- Each shot carries narrative beat, camera grammar, action chain, sound, transition, and ending state.

Phase 5 Model Adapter:

- Compile to Seedance Prompt, Kling Prompt, Veo Prompt, Runway Prompt, Pika Prompt, Sora Prompt, or Midjourney Video motion prompt.

## Template Pattern Library

Use this as the compressed version of the external template library. Select a pattern by dramatic function, then replace placeholders and keep each generated segment independently complete.

Universal prompt skeleton:

```text
【基础风格】: project-level camera/lens look, focal/depth behavior, color/texture/genre baseline, plus scene-specific lighting source/direction/contrast, atmosphere, and material response. Required in every independent segment; never write only "同上".
【角色/场景/素材锁定】: character identity, scene identity, props, color card, voice/audio anchors, and every @image/@video/@audio role. Assign short locked names; state exclusions only when ambiguity, conflict, protected identity/brand/voice, audio leakage, or drift risk makes them necessary.
【运镜与时间轴】: each time beat includes duration rationale, shot type, camera position, shot size, movement, frame structure, composition, focus path, marker, sound cue, cut reason, and ending state. Use locked names instead of repeatedly calling @references.
【声音设计】: environment/action/dialogue only; no background music unless requested.
【画面限制】: concise model failure prevention rules.
NEGATIVE RULES: identity drift, beauty filter, extra text, random motion, unsupported style.
```

Template selector:

| Template pattern | Use for | Core rule |
|---|---|---|
| Color Palette Reference Card | project palette, character/environment/creature colors | render HEX swatches and function labels; no gradients, no texture |
| Film Still Prompt | key frame, poster base, first-frame reference | concept + anchors + composition + pose + physical detail + light + avoid rules |
| Continuous Macro Push-in | insects, skin, particles, microscopic drama | state size ratio; macro subject remains physically tiny |
| Telephoto EWS Reaction Action | absurd escape, deadpan contrast, far reaction | extreme wide, long-lens compression, big body action |
| Stabilized Dolly-Back Contrast Chase | pursuit contrast, comedy chase | stable foreground tracking contrasts chaotic background |
| Narrative Orbit Voice-over | reasoning, internal monologue, investigation | non-diegetic VO; lips do not move; orbit reveals clues |
| Two-Character Wake-Up | relationship setup, absurd awakening | empty frame first; A/B enter from fixed sides; contained reaction |
| Worldbuilding Establishing Environment | settlement/city/base exterior | geography -> architecture -> function object -> life traces |
| Nomadic Settlement Grammar | tribe/camp/caravan | center ring, residence ring, production ring, edge identity |
| Wardrobe Reference Plate | costume system | complete outfit sets, unified silhouette, material and rank logic |
| Character Interior Layout Plate | bedroom/workshop/private room | top-down 90 degrees; daily objects reveal identity |
| Lateral Market Tracking Crowd | city/crowd/culture | lanes, stalls, foreground occlusion, crowd direction |
| Low-Angle Dialogue Reveal | power dialogue, hidden figure | low angle reveals relation and background clue |
| Top-Down Tabletop Dialogue | map, ritual, conspiracy | table geometry and hand placement carry information |
| Deadpan Reaction Shot | dry comedy, robot/symbol acting | face remains still; small symbol or object carries reaction |
| Three-Beat Escalation Sequence | narrative upgrade | setup -> information device -> emotional decision |
| Sand-Burst Monster Chase | buried creature pursuit | sand surface -> burst -> chase vector -> ending threat |
| Mechanical Arm Body-Scan Fall | scan, restraint, medical/mechanical danger | scanning action, body contact, falling result |
| Four-Shot Rescue Chain | rescue action | slip -> grab -> force -> completed rescue |
| Spielberg Reveal | creature/miracle/threat | reaction before answer; partial detail before full reveal |
| Omen Montage | disaster warning | environment anomaly -> object anomaly -> animal anomaly -> human recognition |
| Hero Orbit Cataclysm | hero facing disaster | orbit around hero, then pull scale into catastrophe |
| Stratosphere God-Scale Disaster | divine/cosmic disaster | high altitude scale, atmospheric layer, tiny world reference |
| Threat Trajectory Realization | trajectory calculation, warning | observe -> judge -> calculate -> fear -> command |
| Evacuation Chaos Montage | panic/crowd collapse | fragments each keep direction and purpose |
| Human Cost Inserts | disaster emotion | mother, elder, youth, merchant, child; one human cost per insert |
| Surface Horror Swarm | parasites, skin horror | surface sign -> rupture -> swarm flow -> body reaction |
| Close-Quarters Survival Combat | compact fight | contact points and target anatomy must be visible |
| Disaster Absurd Comedy | flaw-driven comedy | serious danger, comic result from character flaw |
| Creation-of-Adam Contact Standoff | mythic contact | hand distance, hesitation, silence, symbolic scale |
| Side-Scroll Action | stable action for video models | subject centered, screen direction fixed, run-hit-continue |
| Aerial Assist Side-Scroll | team relay, airborne action | arc, catch point, timing, continuation |
| Anime Transformation Bank | reusable transformation | identity -> trigger -> local change -> full assembly -> final pose |
| Titan Struggle | giant wrestling, hold-and-strain | human scale, grip point, surface failure, strain sound |
| Psychic Echo Cut | fate/memory/cross-space link | same gesture or sound bridges two spaces |
| Music Beat-Matching Route | MV, dance, montage, rhythm ad, action rhythm control | audio controls beat grid, motion accents, cut markers, impact timing, or final BGM style; timeline names marker, cut, motion accent, and ending pose for each major beat; state whether reference audio is output or silent guide; do not let music erase story clarity |
| Product / Food / Object Showcase Route | e-commerce, product ad, material reveal | product identity and proportions locked; camera shows material, separation/assembly/use case, clean background, controlled highlights, SFX bound to object motion |
| Science / Education / Comic Adaptation Route | medical CGI, explainer, manga/storyboard adaptation | simplify to one concept chain; for comic/storyboard use panel order for shot sequence only, not rough drawing style unless requested |
| Distant Horde Emergence | herd/army/monster mass | horizon line, dust wake, scale growth, crowd response |
| Atompunk Zombie-Cleaner Bible | retro-future zombie comedy romance | era, outbreak, machine protagonist, absurd contrast, lonely romance core |
| Mounted Chase + Background Horde | ostrich/animal/vehicle chase with zombies or crowd | foreground rider readable, background horde varied speed, prop throw, delayed blast |
| Six-Enemy Gun-Fu Chain | revolver/melee fight against numbered enemies | number enemies, assign time windows, track bullets, contact points, final state |
| LED-Face Robot Performance | robot with display face instead of human face | static pixel expression states; body rhythm and screen-switch SFX carry emotion |
| Absurd Apocalypse Romance | tender romance inside violent ruined world | romantic action stays sincere; comedy comes from environment mismatch |
| AI Actor Boot-Up | AI performer wakes in abstract space | black void, system boot SFX, confused body calibration, camera-as-sky awareness |
| Prompt-World Scene Loading | generated world appears around actors | external Enter key -> wireframe grid -> environment assets load in order -> actors react without moving position |
| Reference-Reading Dialogue | characters read unseen prompt/reference instructions | characters look into camera/sky; no visible text; dialogue carries information |
| Short-Drama Reference Board Pack | reference photos + rough storyboard + dialogue/OS/language rules | board controls shot order/axis/motion only; photos control scene detail; split into independent 15s A/B Seedance segments |
| Costume Hot-Swap Loading | actor outfit changes from initial to story costume | hide face during change; show shoulders/back/waist/shoes; preserve body and hair identity |
| Real-World Creator Cutaway | creator submits or rewrites prompt | back-view desk scene, screen/keyboard action, no readable UI dependency |
| Pose-Locked Whisper Callback | character breaks scene while pretending still | keep reference pose locked; only eyes/lips/breath move; dialogue is diegetic whisper, not VO |

### Practical Storyboard Micro-Routines

Source: 13 Chinese storyboard-routine explainer videos, extracted from audio transcripts plus representative frames. Use this as a silent selector, not as visible analysis. Do not copy source characters or exact scenes; translate the mechanism into the user's story.

| Routine | Trigger | Silent structure to compile into prompts |
|---|---|---|
| Face-to-Face Occlusion Reveal | two people meet, confront, confess, negotiate | follow A from behind -> A's back blocks the object/person ahead -> camera slides away to reveal B -> A single, B single, two-shot -> characters exit and leave a meaningful center object/empty frame |
| Duel Time-Stretch |高手对决, one decisive strike, weapon standoff | do not only show one hit; stretch preparation with 3 weapon/body-action inserts; mirror down-tilt/up-tilt or left/right placement; give the active protagonist a close-up immediately before contact; return to fair symmetrical frame for result |
| Four-Level Escape | chase, surrounded, route blocked, action comedy escape | level 1 improvised weapon from foreground; level 2 obstacle enters escape route; level 3 height drop with top-down/ground POV hesitation; level 4 reinforcements arrive from different screen directions, then switch from objective coverage to tracking shot only at life-or-death escape |
| Farewell Spatial Separation | breakup, departure, leaving home/team, impossible decision | make courage and received pain visible through distance, road, tree/doorframe separator, sky/land contrast, held silence after the decision; leaving person usually owns screen-right/far road/sky, staying person owns ground/left/blocked frame |
| Hostage Rescue / Divine Arrival | save the victim, punish villains, mysterious rescuer | show villain cruelty first: medium action impact -> wide reveal of villains -> victim close-up/tears -> weapon enters before wielder reveal; rescuer appears as blur/light/wind before face; after each takedown cut to villain reaction; reveal rescuer last |
| Weak Hero Stands Up | small character protects someone stronger villain threatens | weak hero enters from behind occluder; use victim high-angle helplessness and villain low-angle power; when villain moves, camera follows villain to show scene control; repeat high/low reverse shots for dialogue; defeat may be ugly but earns partial moral goal |
| Repeating Task Montage | overwork, chores, delivery, training, bureaucracy, daily pressure | establish one repeatable action normally; repeat it with visible variation in prop color/size, location, camera, motion direction; after fast repeats insert one 4-5 shot slower complication; accelerate with stacked dialogue/music; close with the opening push-in/callback |
| Defeat-to-Transformation Resolve | beaten hero, rebirth, awakening, power-up | defeated body cannot move -> villain/unknown truth fills pressure -> internal monologue -> down-tilt into empty mental space -> imagined figure approaches through repeated cuts -> eye-to-eye match -> reality push-in -> fast pull-back with effect -> white flash -> bystander explanation, environment reaction, villain test hit, final form |
| Street-Corner Search / Lost Target | lost lover, target disappears, city pursuit | character loses sight, stops at corner, looks left/right; POV search finds nothing; terrain height or tunnel creates visual focus shift; reacquire target, use lateral running shot with occluders to tighten scale; extend final hand/reach hesitation with face and hand inserts |
| Shock Arrival / Impossible Person | dead person returns, undercover appears, secret witness, shock | start from back of head or small body part; off-screen voice leads; push-in then jump-cut closer to create sudden magnification; if stealthy, keep characters silent and static on diagonals; use footstep inserts and unreal sound; subject's shots can use extreme high/low angles while bystanders stay level |
| Planned Long-Take Route | one-shot meeting, bridge/walkway/office corridor, group splits or gathers | choose a naturally routed space; begin with fixed empty frame; actors enter and camera only keeps them in balanced composition; design internal markers: hit, stop, talk, split, bird/object cue, exit; reverse the route to turn departure into gathering |
| Object-and-Mirror Monologue | one person talks, self-address, confession, rehearsal | begin with 3-4 object close-ups under dialogue; reveal speaker as if addressing camera; pull back to show mirror/reflection, turning monologue into self-dialogue; give hands a small task; let another person/object enter mirror edge to interrupt or escalate emotion |
| Parallel Desire / Color-Object Association | love triangle, temptation, memory, conflicting choices | one solo action provides base rhythm; insert two parallel spaces at action joins; assign each relationship a color/object/material; repeat action close-up -> face -> alternate memory/world; proportion of action spent on each color/object reveals inner weight |

Micro-routine compile rules:

- Always translate the routine into concrete frame structure: screen-left/right, foreground/midground/background, occluder, route, focus path, body part, reaction shot, cut reason, and ending state.
- The routine chooses the story logic; the final Seedance prompt still needs full character/scene/style locks and per-segment independence.
- For live action, avoid overusing anime-only camera extremes. Keep the function but moderate the movement, angle, and VFX.
- If one routine exceeds 15 seconds, split at a natural phase boundary: reveal/result, obstacle/result, decision/aftermath, transformation/final form.

Template use rules:

- A template is a director structure, not a fixed script. Replace story content, do not copy nouns blindly.
- If a template contains multiple beats, split it for Seedance when it exceeds 15 seconds.
- For reference-generation templates, lock layout, labels, HEX, material, and object categories.
- For video templates, lock camera continuity, spatial direction, action chain, sound, and ending state.
- When a template uses dialogue or voice-over, state whether it is diegetic or non-diegetic and whether lips move.

## 2. Source Analysis Engine

Extract before writing prompts:

- Story premise: what changes in the scene?
- Character goal: what each important character wants now.
- Conflict: who or what blocks the goal.
- Emotional temperature: calm, dread, desire, awe, panic, grief, absurdity.
- Scene geography: entrances, exits, object positions, crowd flow, danger line.
- Time/weather/material: day/night, rain/dust/fog, stone/metal/cloth/skin/glass.
- Timeline beat design: shot function, duration range, information density, motion intensity, attention track, marker, transition type, sound bridge, and emotional hold/release.
- World rules: realistic, mythic, sci-fi, supernatural, comedic, disaster.
- Visual anchors: face, costume, silhouette, props, locations, palette, creature form.
- Model constraints: duration, aspect ratio, reference image usage, language, platform.

Convert prose into visible beats:

- "He realizes the truth" -> eye freeze, breathing stops, background sound drops, slow dolly in.
- "The city panics" -> front row looks up, second row backs away, rear crowd runs toward gate, cart blocks exit.
- "The monster appears" -> sound first, shadow second, body fragment third, human reaction fourth, full scale fifth.

Existing prompt diagnosis:

- Missing STYLE LOCK at the front.
- Missing character/scene anchors.
- Too many events in one shot.
- Timeline uses arbitrary equal-length beats instead of motivated shot durations.
- Shot duration conflicts with information density, action readability, dialogue length, or emotional hold.
- No camera position or movement.
- No spatial relationship.
- No action causality.
- No lighting source and material reaction.
- No sound confirmation.
- No ending state for continuity.

## 3. Segmentation Engine

Beat-to-segment rules:

- First create fine storyboard beats for information order, camera logic, action causality, and sound cues.
- Then pack beats into Seedance generation segments. The segment is the output prompt block; the beat is only an internal time-axis unit.
- Default packing target: `5-15s`, preferably `12-15s` when readable.
- Pack together: continuous action, same speaker, same primary character, same location, same time state, same emotional direction, or sound-bridged continuity.
- Split early only when the scene/location changes, shot scale or camera setup changes enough to confuse the model, primary character/speaker changes, physical geography must be re-established, time state changes, or a causal action unit ends.
- Do not split only because a new micro fact appears, a reaction happens, or the storyboard would traditionally cut to a close-up. Keep those as internal time beats if they remain in the same continuous scene.
- For Seedance, split before 15s and make each segment independently complete.
- Segment boundaries use ending state plus opening re-anchor, not default transition effects. Avoid same-character/same-shot-scale/same-composition across a segment boundary.
- If a crowd or background extras continue across beats or segments, repeat the crowd density, screen layer, flow direction, congestion point, and visibility; write `background crowd remains softly blurred but visible` when the crowd is not the focus but must persist.

Default segment lengths:

| Segment type | Use for | Default length |
|---|---|---:|
| Packed scene unit | same location + same speaker/character + continuous story | 8-15s |
| Action unit | one causal physical chain | 6-15s |
| Dialogue / monologue unit | one person or exchange in same space | 6-15s |
| Establishing + pressure | location, scale, danger geometry, first pressure | 5-12s |
| Reveal + reaction | object/truth/world plus immediate human response | 5-12s |
| Montage | compressed multi-info sequence | 5-15s total, with internal 0.5-2s beats |
| Transition bridge | sound/image bridge to next scene | 5s only if it must stand alone; otherwise attach to previous or next segment |

Continuity ledger per segment:

```text
CHARACTER LOCK:
SCENE LOCK:
SCREEN DIRECTION:
STARTING STATE:
ENDING STATE:
NEXT SHOT HOOK:
```

## 4. Director Framework Selector

Choose a framework by scene function and translate it into concrete rules.

| Framework | Use when | Concrete rules |
|---|---|---|
| Spielberg Reveal | creature, threat, miracle, secret | sound first -> reaction -> partial detail -> environmental effect -> full reveal -> final reaction |
| Omen Montage | disaster warning, supernatural approach, invisible threat | environment anomaly -> object anomaly -> animal anomaly -> human recognition -> truth reveal |
| Threat Realization | trajectory, incoming danger, tactical warning | observe anomaly -> judge path -> calculate consequence -> fear -> warning command |
| Human Cost Inserts | disaster needs emotion and stakes | insert one person fate at a time: mother protects child, elder accepts fate, youth shields others, merchant clings to goods, child freezes |
| Hero Orbit Reveal | hero or protagonist must face overwhelming event | low-angle orbit around hero; character reaction appears before audience sees full threat |
| Dune Scale / Villeneuve Scale | desert, fog, sacred space, giant object, fate | tiny human reference, low horizon or massive negative space, slow camera, deep atmosphere, restrained emotion |
| Mad Max / George Miller Action | chase, escape, battle route, kinetic comedy | center-frame subject, readable screen direction, one action vector, fast result confirmation, hard cuts |
| Hitchcock Realization | dread, truth, vertigo, trap | slow push-in or dolly zoom only at the realization moment, isolate face, sound narrows |
| Kurosawa Weather Blocking | war, mud, wind, group pressure | weather direction matches conflict, group moves as force, flags/clothes/dust show vector |
| Fincher Procedural Tension | investigation, conspiracy, cold dread | controlled locked-off frames, precise inserts, low-key practical light, minimal expression |
| Wong Kar-wai Memory Emotion | longing, missed timing, interior loneliness | step-print or slow motion, reflective surfaces, saturated accent color, repeated gesture |
| Documentary Witness | panic, realism, survival | 16mm/handheld feel, imperfect exposure, reactive framing, sound over polish |
| Rescue Chain | falling, last-second rescue, teamwork | mistake -> slip/fall -> grab point -> force/strain -> recovery or failure result |
| Side Scroll Action | stable running combat, Seedance-friendly action | run -> hit -> keep running -> second obstacle -> transition; screen direction never flips |
| Absurd Contrast Romance | apocalypse, comedy, loneliness, non-human affection | place leisure/romance behavior against corpses, ruins, or danger; keep emotion sincere |
| Mechanical Loneliness Arc | robot/android gains self-awareness | repetitive cleanup duty -> private celebration -> scare/comedy beat -> companion discovery -> tender routine |
| AI Actor Meta-Comedy | characters know they are being generated or directed | external prompt/keyboard sound becomes story trigger; actors react as performers trapped in production logic |
| Prompt Failure Realization | character detects reference/image mismatch or bad generation | inspect body/hands/costume -> delayed realization -> restrained dolly zoom or exhausted reaction |

Never rely on director names alone. Name the visible mechanics.

## 5. Director Knowledge Base Extensions

Use this section as the compact Phase 2 knowledge base. It prevents the system from becoming only a prompt library.

### Cinematographer logic library

Do not imitate a person by name alone. Choose the cinematography logic:

- Naturalist drama: soft highlight rolloff, truthful skin, quiet lensing, motivated practical light.
- Large-format scale: wide frame, tiny human reference, deep atmosphere, slow reveal, monumental negative space.
- Neon noir: clean dark shadows, wet reflections, color-separated rim lights, controlled contrast.
- Documentary witness: imperfect exposure, handheld reaction, available light, urgent body sound.
- Commercial precision: sharp product/action clarity, clean surfaces, controlled highlights, high readability.
- Film memory: grain, halation, imperfect texture, warm density, soft temporal feeling.
- Prestige suspense: low saturation, shallow depth, restrained camera, small facial changes.

### Style film archetypes

Use archetypes to select language without overloading prompts with film names:

- Desert-scale sci-fi: Dune Scale, harsh sun or firelit interior, large-format width, low-frequency rumble.
- Rain-night urban crime: Sony VENICE style, neon reflection, wet asphalt, rim light, distant siren bed.
- Korean prestige suspense: Mini LF + Signature Prime style, low saturation, clean face closeups, quiet push-in.
- Vintage period realism: 35mm film grain, practical lamps, patched fabric, smoke marks, class markers.
- Game/VFX boss trailer: RED/Tokina clarity, centered hero action, energy burst, armor detail, impact sound.
- Corporate technology film: modern industrial order, clean lines, high-key controlled light, precise movement.
- Lifestyle warmth: Canon/Sumire softness, natural window light, gentle skin, small domestic sounds.
- Hollywood spectacle: Primo 70 width, heroic low angle, heavy spatial pressure, orchestra-like sound mass if music is needed.

### Monster library

Define creature type before reveal:

| Creature type | Reveal logic | Movement logic | Sound logic | Prompt focus |
|---|---|---|---|---|
| Landscape giant | mountain/island detail moves first | slow tectonic motion | deep whale-like moan, ground rumble | tiny human scale, dust, shadow crossing terrain |
| Pack predator | one silhouette, then many eye points | fast lateral crossing, encirclement | chittering scuttle, claw scrape | escape gaps, threat directions |
| Armored boss | partial armor plate, weapon limb, full body | heavy stomp, delayed turn | metallic shell scrape, impact bass | contact points, weak seams, VFX clarity |
| Parasite swarm | small sign first, then surface crawling | wave-like spread | insect skitter, wet cluster sound | density, direction, body reaction |
| Sacred/divine beast | environmental silence, light exception, impossible scale | calm non-human rhythm | low chant-like resonance | awe before threat, color exception |
| Mechanical-organic hybrid | servo detail, wet tissue, blinking UI | hydraulic twitch then full motion | servo whine + wet breath | material contrast and malfunction points |
| Invisible force | object reaction before subject | pressure wave, dust displacement | silence then low-frequency pulse | environment deformation, character reaction |
| 地龙 / world-scale earth dragon | world-level natural disaster | horizon bulges, city-scale ground displacement | blue-whale low-frequency moan + earthquake rumble | far distance still enormous; compare to city or mountain |
| 龙虱 / parasite swarm | waist-high parasite swarm | group skitter, sudden surface rupture | dense chittering scuttle | swarm density, flow direction, skin/body reaction |
| 甲壳兽 / migrating armored herd | natural migration, living disaster | slow group push from horizon | shell scrape + heavy ground stomp | herd route, dust wake, non-random ecology |

## 6. Photography Style Generator

Select one photography style based on subject and atmosphere, then translate equipment style into concrete image description in the final prompt.

Mandatory conversion rule:

```text
Bad: ARRI ALEXA 35 + Cooke S4/i
Good: 画面具有宽动态范围、柔和高光过渡、真实肤色、自然暗部层次、专业影视剧组布光。
```

| Subject / mood | Camera and lens style | Visible image description to write into prompt |
|---|---|---|
| 真实电影感、专业剧组感 | ARRI ALEXA 35 + Cooke S4/i | 宽动态范围、柔和高光、真实肤色、厚实暗部、自然暗部层次、专业影视剧组布光 |
| 高级韩剧、偶像悬疑、人物情绪 | ARRI ALEXA Mini LF + ARRI Signature Prime | 大画幅干净高级、低饱和、肤色自然、浅景深、背景柔和分离、情绪克制 |
| 雨夜、霓虹、都市犯罪 | Sony VENICE 2 + Zeiss Supreme Radiance | 夜景暗部干净、霓虹反射、冷暖混合光、轮廓光明显、湿地面高光 |
| 游戏广告、BOSS战、爆装备、VFX | RED V-RAPTOR XL + Tokina Vista | 高分辨率、锐利动态、动作清晰、特效密度高、金属和能量边缘清楚 |
| 企业科技宣传片 | ARRI Mini LF / Canon Cinema EOS | 干净专业、可信、现代工业秩序感、柔和受控高光、空间整洁 |
| 温情人物、生活方式广告 | Canon Cinema EOS + Canon Sumire | 肤色温柔、自然光、亲和真实、柔和反差、生活质感 |
| 复古年代、胶片感 | ARRICAM 35mm Film + Cooke S4/i | 胶片颗粒、柔和高光、厚实暗部、复古色彩、轻微卤化和不完美质感 |
| 史诗奇幻、大场面 | ARRI ALEXA 65 + Prime 65 | 65mm大画幅、宏大沉浸、空气感强、人物与世界尺度清楚、空间纵深深 |
| 好莱坞商业大片 | Panavision DXL2 + Primo 70 | 宽银幕、华丽厚重、英雄感、空间压迫、干净大制作质感 |

Expanded camera/lens packages:

| Camera body | Lens group | Focal range | Aspect ratio | Depth / distortion | Best for |
|---|---|---|---|---|---|
| ARRI Alexa 35 | Cooke S8/i or S4/i | 35/50/75mm | 1.85 or 2.39 | soft skin, warm rolloff, shallow natural depth | drama, faces, natural daylight |
| ARRI Alexa LF | Panavision Ultra Panatar | 40/50/65mm | 2.39 or 2.76 | large-format width, creamy falloff | desert, sacred scale, mythic travel |
| Sony Venice 2 | Primo 70 or Supreme Radiance | 35/50/85mm | 2.00 or 2.39 | clean night shadows, reflective surfaces | sci-fi, neon city, rain night |
| RED V-Raptor XL | Atlas Orion or Tokina Vista | 32/40/65mm | 2.39 | sharp, contrasty, flare or VFX clarity | action, commercial, game trailer |
| IMAX 65/70mm language | large-format spherical | 28/35/50mm | 1.43/1.90/2.20 | immense vertical scale, deep clarity | miracles, disasters, cosmic scale |
| 35mm Kodak Vision3 | vintage spherical/anamorphic | 28/35/50mm | 1.85 or 2.39 | grain, halation, warm density | memory, village, road, smoke |
| 16mm documentary | lightweight prime/zoom | 18/24/35mm | 1.66 or 1.78 | rough grain, imperfect exposure | panic, witness footage, survival |

Focal length rules:

- 14-18mm: foreground distortion, panic, cramped interiors, subjective unease.
- 24mm: environmental human scale, establishing, crowd with protagonist.
- 35mm: natural drama, walking, discovery, balanced space.
- 50mm: intimate face, calculation, controlled reaction.
- 75-100mm: compression, isolation, distant threat feels closer.
- 135mm+: heat haze, battlefield density, far giant threat.

## 7. Shot Grammar

Shot sizes:

- ECU 极特写: eye, finger, blood, symbol, micro-reaction.
- CU 特写: face emotion, object importance.
- MCU 中近景: dialogue, controlled reaction, shoulders visible.
- MS 中景: body language, prop use.
- MLS 中远景: full body plus environment.
- WS 全景: geography, route, crowd direction.
- EWS 大远景: scale, world, disaster, isolation.

Angles and perspectives:

- OTS over shoulder: relationship, confrontation, looking direction.
- POV: subjective fear, discovery, embodied movement.
- Top-down 90 degree: crowd pattern, maze, disaster geometry.
- Low-angle: power, giant scale, hero/monster dominance.
- Dutch angle: disorientation only, not generic style.
- Locked-off: ritual, dread, observation, precise comedy.
- Handheld: panic, documentary, unstable danger.
- Steadicam: controlled pursuit, elegant travel.
- Crane: vertical scale reveal.
- Drone/aerial: migration, battle route, city geography.

Axis rule: preserve screen direction unless confusion is intentional. If the protagonist moves right in 第01段 / beat 01, the pursuit should maintain rightward progress or clearly reset geography.

## 8. Camera Movement

| Movement | Emotion / story use | Wrong use | Prompt kernel |
|---|---|---|---|
| slow dolly in | attention, realization, pressure | action geography | `镜头缓慢推进 slow dolly in toward the face` |
| fast dolly back | shock, sudden scale, loss of control | gentle sadness | `fast dolly back revealing danger` |
| lateral truck | travel, side-scrolling action, crowd flow | static reaction | `lateral truck, subject stays centered` |
| orbit | ritual, trapped character, 3D object reveal | simple walking | `orbit around the subject` |
| descending spiral orbit | falling, cursed revelation, vertical dread | normal dialogue | `descending spiral orbit, camera circles downward` |
| crane rise | sacred architecture, disaster scope | small prop reveal | `crane rise revealing the whole settlement` |
| tilt up reveal | human to giant, object to sky | no vertical information | `tilt up reveal from feet to towering body` |
| push-in tension | threat closing, decision pressure | calm establishing | `push-in tension, shallow breathing` |
| pull-back scale reveal | human-to-world contrast | close emotional climax | `pull-back scale reveal, tiny human scale` |
| handheld panic | crowd collapse, chase, impact | clean hero pose | `handheld panic, unstable frame` |
| steadicam glide | controlled discovery, elegant pursuit | impact chaos | `steadicam glide through market crowd` |
| whip pan | fast attention shift, surprise | slow drama | `whip pan from scream to source` |
| rack focus | shift attention between planes | both subjects must be clear | `rack focus from foreground hand to distant monster` |
| bullet time | impossible impact emphasis | routine punch | `bullet time, suspended debris` |
| Hitchcock dolly zoom | truth realization, dread | generic fear | `dolly zoom as character realizes the truth` |

### Camera Movement Semantics Library v3

Purpose: choose movement for what it does to story perception, not because the term sounds cinematic.

| Movement | Narrative function | Emotional function | Frame requirements | Prompt kernel |
|---|---|---|---|---|
| locked-off stillness | evidence, inevitability, institutional coldness | pressure through lack of escape | strong composition, meaningful foreground/background, actor motion carries change | `locked-off camera, no movement; only the character's breath and hand reveal the pressure` |
| slow push-in | move audience toward a clue or realization | tightening attention | clear end target; focus path must land on face/object | `slow push-in toward [face/object], ending on the exact realization point` |
| slow dolly in | pressure, intimacy, dread | emotional squeeze | stable axis, shallow but readable depth | `slow dolly in, background threat stays fixed while the face grows larger` |
| fast dolly back | sudden scale, loss of control, shock | fear/exposure | reveal new space or threat behind/around subject | `fast dolly back revealing the subject is surrounded by [space/threat]` |
| lateral tracking / lateral truck | continuous travel, chase, procession, side-scroller action | momentum and readability | screen direction locked; subject relation to background changes | `lateral tracking shot, subject remains centered, background obstacles pass screen-right to screen-left` |
| crane rise | reveal scale, fate, isolation, aftermath | awe or loneliness | start with human/object, end with geography or crowd | `crane rise from the character to reveal the entire danger field` |
| crane rise from face to overhead scale reveal | move from private emotion to system/environment scale | small person under large fate | start on face/body, end as map-like danger geometry | `crane rise from the face into an overhead scale reveal, turning personal fear into visible geography` |
| crane descend | judgment, pressure from above, fate closing in | oppression | begin with map-like view, descend to trapped subject | `crane descend from overhead layout into the trapped subject's face` |
| crane descend into danger pocket | show the trap before the character understands it | dread, inevitability | begin with escape routes/hazards, descend to subject inside the trap | `crane descend into the danger pocket, overhead layout collapses into the trapped subject` |
| top-down overhead | explain geometry, crowd pattern, maze, accident mechanics | detached, system-like control | routes/exits/hazards must be visible | `top-down overhead view showing route, obstacle, exit, and danger line` |
| top-down tactical overhead | crowd/action planning, accident causality, pursuit routes | chessboard pressure | screen-left/right routes, choke point, counterflow, hazard line visible | `top-down tactical overhead showing main route, counterflow, choke point, exit, and danger line` |
| god's-eye overhead stillness | fate, institutional coldness, powerless figure | human as small marker | subject isolated inside strong geometry | `god's-eye overhead stillness, the subject appears like a small mark inside the rigid layout` |
| orbit | establish subject as center, ritual, inspection | awe, obsession, unease | subject must hold center; background changes meaning | `orbit around the still subject as background clues rotate into view` |
| 360 table orbit | negotiation, judgment, family rupture, conspiracy | shifting power circle | table edge and hands remain readable | `slow 360 table orbit, power moves from one seated body to another through hands, eyelines, and silence` |
| spiral orbit | psychological fall, curse, dizziness, destiny closing | loss of control | vertical change plus rotation; do not use for normal dialogue | `descending spiral orbit around the subject, space tilts into psychological collapse` |
| threshold push-through | world-state transition, entering danger, crossing taboo | point of no return | camera passes through door/curtain/window/smoke/vehicle frame | `threshold push-through through [door/curtain/smoke], crossing from safe space into threat space` |
| foreground wipe transition | hidden cut, time jump, location shift, memory bridge | smooth but motivated transition | foreground object must naturally pass frame | `foreground wipe transition as [person/cloth/vehicle/pillar] crosses the lens, revealing the new beat` |
| crash zoom / snap zoom | sudden clue, absurd turn, surprise danger | attention shock | target must be simple and high-value | `snap zoom to [clue/threat/face] the instant the sound reveals it` |
| long-lens compression stalk | pursuit, surveillance, distant threat feels close | pressure, inevitability | flattened background, subject and threat appear closer | `long-lens compression, distant threat seems to press directly behind the subject` |
| wide-angle proximity distortion | cramped panic, intimacy, grotesque pressure, absurdity | too-close instability | close camera, edges distort, body/space still readable | `wide-angle close camera, foreground hands and face feel too close, room edges bend slightly` |
| whip pan | urgent attention shift, surprise, reveal, comedy turn | shock, snap realization | start and end targets must be simple | `whip pan from the reaction face to the source of the sound` |
| rack focus | transfer information or power between planes | sudden understanding | both start and end subjects named | `rack focus from foreground hand to background witness` |
| dolly zoom / Hitchcock dolly zoom | truth realization, vertigo, impossible space anxiety | dread, disorientation | face must freeze while background warps | `Hitchcock dolly zoom, camera dollies in while zooming out, background stretches away from the frozen face` |
| bullet time | decisive instant, super-perception, impossible action | suspended shock | particles/fabric/debris show slowed time; use sparingly | `bullet-time feeling, camera orbits suspended action while dust and fabric hang in air` |
| speed ramp | impact choreography, epic contact, sudden acceleration | violent emphasis | slow before contact, normal/fast at impact, hold aftermath | `speed ramp slows before contact, snaps to real speed on impact, then slows on the aftermath` |
| snorricam | subjective instability, intoxication, panic, dissociation | world moves around fixed body | character locked to camera, background moves | `snorricam feel, character locked in frame while the world sways behind them` |
| handheld panic | survival urgency, collapse, documentary witness | fear and instability | imperfect but readable; do not hide contact points | `handheld panic, reactive framing follows the body stumble without losing the contact point` |
| steadicam glide | controlled discovery, ghostly pursuit, elegant danger | fate-like smoothness | route must be continuous; background events can unfold | `steadicam glide through the corridor, camera follows behind as off-screen sound grows louder` |

Common errors:

- Using crane rise for a small prop instead of scale, aftermath, or isolation.
- Using bullet time for routine action with no decisive moment.
- Using dolly zoom as generic fear without a truth realization.
- Using handheld shake to hide unclear action; contact points must remain readable.
- Using orbit around moving dialogue without a ritual, inspection, obsession, or reveal reason.
- Using crash zoom when the target is not a new clue, threat, or comic reversal.
- Using a long take without internal beat compartments; a useful oner still needs route, obstacle, reveal, reversal, and ending state.

Selection rule:

```text
CAMERA MOVEMENT SEMANTICS: choose [movement] because the story needs [information transfer / scale reveal / power shift / realization / time distortion / action continuity / emotional pressure / danger discovery / route clarity], not because it looks cinematic. State start frame, path, end frame, focus owner, and hold/cut reason.
```

## 9. Lighting System

Lighting formula:

```text
light source + direction + intensity + shadow behavior + atmosphere + material reaction
```

Presets:

| Lighting | Use for | Prompt phrase |
|---|---|---|
| Dune daylight harsh sun | desert, scale, survival | `harsh overhead desert sun, hard short shadows, dust haze, bleached stone highlights` |
| Dune firelit interior | ritual, cave, ancient chamber | `low firelit interior, orange flicker from below, smoke softens shadows, rough stone catches warm edge light` |
| golden hour | memory, hope, farewell | `low golden hour backlight, long shadows, warm rim light on hair and fabric` |
| blue hour | melancholy, pre-battle | `blue hour ambient sky, cool soft fill, readable silhouettes` |
| moonlight | secrecy, nocturnal travel | `cool moonlight from upper left, silver rim light, deep blue shadow pockets` |
| oil lamp | poverty, handmade world | `single oil lamp key light, weak amber pool, room falls into soft darkness` |
| candlelight | ritual, prayer | `candlelight flicker, tiny warm highlights in eyes, unstable wall shadows` |
| torchlight | pursuit, cave, panic | `moving torchlight, flickering orange side light, shadows crawl across faces` |
| neon | cyberpunk, temptation | `neon magenta and cyan side light, wet pavement reflections` |
| fluorescent | office, hospital | `overhead fluorescent tubes, greenish cast, harsh eye sockets` |
| overcast natural light | realism, grief | `overcast natural light, soft shadowless sky, desaturated texture` |
| skip-bleach contrast | war, disaster | `skip-bleach contrast, crushed blacks, silver highlights, low saturation` |
| documentary natural light | handheld realism | `available light only, imperfect exposure, documentary realism` |
| low-key horror lighting | concealment, suspense | `narrow side key, black negative fill, details hidden in shadow` |
| high-key commercial lighting | product, beauty | `high-key softbox lighting, minimal shadow, controlled glossy highlights` |

Material response:

- skin: sweat catches rim light, cheekbone specular highlight, warm shadow on skin.
- fabric: linen absorbs light, silk catches narrow highlight, wool stays matte.
- metal: cold edge highlights, scratched glints, dull oxidized bronze.
- stone/clay: rough texture catches side light, dusty stone blooms under harsh sun.
- water/glass: broken reflections, neon streaks, specular shimmer.
- smoke/dust/fog: volumetric shaft, dust reveals beam, smoke softens shadow edge.

## 10. Color System

Use color as story logic, not decoration.

Palette formula:

```text
60% environment base + 30% character/costume contrast + 10% danger/supernatural/accent color
```

Rules:

- Use HEX locks only for recurring story-critical colors, not every color.
- Character color: identity and continuity.
- Environment color: world pressure.
- Danger color: conflict, threat, taboo.
- Supernatural exception color: breaks the normal palette intentionally.
- Warm/cold relation must show conflict: warm human against cold city, cold moon against warm torch, etc.
- LUT language may be used: `low saturation teal shadows`, `warm film print highlights`, `skip-bleach silver contrast`.

Color card format:

```text
PALETTE: 60% dusty sandstone #B89B6A, 30% indigo cloth #263A5B, 10% supernatural green #6CFFB8.
COLOR LOGIC: environment is dry and ancient, character stays readable, green appears only when fate intervenes.
```

## 11. Sound Design

Sound confirms action and often leads the cut.

Categories:

- environment: wind hum, sand hiss, rain on tarp, market murmur, distant chant.
- action: cloth rustle, leather creak, metallic impact, bone crack, ground scrape.
- body: breath catch, heartbeat thump, swallowed panic, wet cough, foot slip.
- creature: deep whale-like moan, chittering scuttle, wet throat rumble, shell scrape.
- machine: hydraulic hiss, servo whine, turbine swell, engine choke.
- magic/energy: low-frequency pulse, energy surge, energy burst, magical shing, glassy resonance, reverse shimmer.
- UI/tech: electronic bling, soft confirmation chime, static glitch.
- meta-production: keyboard typing, Enter key press, system boot tone, 3D wireframe scan, prompt loading blip, laptop fan.
- disaster: low-frequency rumble, distant collapse, pressure wave, structural groan.
- space: cavern echo, alley slapback, muffled interior, vacuum silence.
- silence: sound drops out at realization, then one tiny body sound remains.
- audio reference: BGM reference, beat grid, ambience bed, SFX reference, narrator voice, character voice.

Sound bridge rules:

- Sound can enter before the image when a scene transition needs anticipation.
- Sound can cut abruptly when shock, blackout, or death occurs.
- Do not add music labels when an action sound would be more useful.
- If the source material asks for realism or tokusatsu/mecha impact, prefer production sound and action sound over background music.
- If an audio or video reference supplies a voice, lock voice separately from face and body: timbre, age impression, accent, speaking pace, emotional delivery, and microphone texture. Repeat the voice lock in every independent Seedance segment where that character/narrator speaks.
- Voice reference does not rewrite dialogue content. Dialogue text still follows the user's script.
- Voice-over, internal OS, or narration must not move lips unless the character is visibly speaking on screen.

Voice lock kernel:

```text
VOICE LOCK: @AudioN / @VideoN audio is the [character/narrator] voice reference; preserve [timbre, age impression, accent, pace, emotional delivery, microphone texture] across this segment. This controls voice only, not face, costume, location, or dialogue content.
```

Sound mapping shortcuts:

- giant object: `deep whale-like moan`, `sub-bass air pressure`, `distant structural groan`.
- earthquake: `low-frequency rumble`, `stone crack`, `dust fall`.
- giant footsteps: `heavy ground stomp`, `delayed dust impact`, `loose debris rattle`.
- audio rhythm guide: `wind whoosh` usually biases speed/dash/camera sweep; `hard drum transient` biases impact/cut-in/contact; `fast repeated transients` bias combo rhythm; `sustained strings or pads` bias emotional hold/slow push; `piano or waltz pulse` biases step-based continuous movement; `rock backbeat` biases close impact and aggressive cut-ins.
- silent guide warning: if @Audio is used only for rhythm, write `reference audio controls motion and cut timing only, do not output it as BGM`; then specify the final audible layer separately.
- insect swarm: `chittering scuttle`, `dry leg scrape`, `dense clicking bed`.
- machine: `servo whine`, `metal groan`, `hydraulic hiss`.
- energy: `energy surge`, `magical shing`, `electric crackle`, `glassy resonance`.
- transformation pain: `forced breath`, `wet tissue stretch`, `electric hiss`, `crystal crack`, `0.1s camera-shake thump`.
- AI actor boot: `system boot tone`, `tiny electric twitch`, `cloth floor rustle`, `confused breath`.
- scene loading: `Enter key click`, `wireframe scanning sweep`, `rain bed gradually rising`, `industrial lamp hum`, `tail-light electric buzz`.
- creator cutaway: `quiet room tone`, `computer fan`, `soft keyboard taps`, `tired sigh`, `clear Enter key downstroke`.

## 12. Editing and Transitions

Every segment after 第01段, and every internal beat after beat 01, needs:

```text
EDIT REASON: [transition] because [new information / emotional shift / viewpoint shift / conflict escalation / scale reveal / action result].
```

Transitions:

- hard cut: clean information step.
- smash cut: shock, comedy, sudden scale.
- match cut: visual continuity across time/space.
- white flash: explosion, divine reveal, overexposure.
- black flash: impact, lost consciousness, blackout.
- fabric wipe: cloth/body passes lens.
- foreground occlusion: object blocks camera for hidden cut.
- sound bridge: next scene enters through sound.
- reaction cut: audience reads event through face.
- psychic echo cut: memory, fate, supernatural link.
- montage cutting: one fact per shot.
- slow-motion insert: sacrifice, decision, key impact.
- speed ramp: acceleration into impact then normal speed.

## 13. Action Choreography

Action formula:

```text
space relationship -> route -> force source -> contact point -> counterforce/failure point -> escalation/charge -> result shot -> aftermath consequence -> sound confirmation
```

### Martial Action Three-Way Router

When the request involves 武戏、打斗、格斗、决斗、兵器、技能、法术或招式, silently choose one primary route:

1. `空手格斗 / UNARMED COMBAT`: punches, palms, elbows, knees, kicks, throws, locks, grappling, ground control, or unarmed multi-opponent action.
2. `武器格斗 / WEAPON COMBAT`: blades, knives, staffs, spears, heavy weapons, shields, firearms in close combat, or weapon-versus-unarmed action.
3. `能量招式 / ENERGY TECHNIQUE`: qi, magic, elements, shockwaves, barriers, weapon infusion, superpowers, transformation skills, or original finishing moves.

These are silent retrieval and compilation modules. They must not create new visible top-level sections. All attack, defense, contact, recoil, recovery, charge-up, collision, and aftermath instructions are bound to exact time windows inside `【运镜与时间轴】`. Do not output a separate `【打斗提示词】`, `【招式说明】`, or default `【动作调度】` section unless the user explicitly asks for an action-design sheet or choreography analysis.

For hybrid combat, select one primary route and at most one secondary route, such as `剑术为主、能量附魔为辅`. Do not spend equal prompt budget on unarmed precision, complex weapon continuity, and dense energy VFX in one generation.

Shared martial-action phase:

```text
意图与预兆 intent / telegraph
-> 发动 initiation / wind-up
-> 接触、格挡或落空 contact / block / miss
-> 反作用 recoil / counterforce
-> 恢复姿态 recovery pose
-> 场面后果 aftermath
```

Readable density guidance:

- `3-5s`: one primary technique or one attack-defense contact.
- `5-8s`: one short exchange chain, usually attack -> defense -> one counter.
- `8-12s`: two or three clear exchange beats with repositioning or recovery between them.
- `12-15s`: three to five simple beats; reduce to two or three when identity, crowd, weapon complexity, or VFX is fragile.
- Each beat has one primary contact target. Do not let both fighters perform unrelated complex combinations at the same time.

Precise martial arts, weapon routines, or complex techniques should prefer an action-reference video. The video controls only assigned motion path, timing, contact rhythm, or camera dimensions; it does not overwrite character identity, costume, location, color, story, or sound. A usable action reference has a clear subject, visible key joints, continuous motion, no internal edit jump, readable contact, and motion slow enough to inspect.

#### Route 1: 空手格斗 / Unarmed Combat

Core principle: use explicit `attack-response`, not simultaneous flailing. For every exchange, decide who initiates, entry side, target point, defensive answer, force direction, and both recovery poses.

Silent ledger:

```text
STANCE / GUARD: lead foot, rear foot, guard, distance.
ENTRY: entry side, depth plane, travel direction.
FORCE CHAIN: ground push -> hip rotation -> torso -> shoulder/elbow/wrist or knee/shin.
ATTACK PATH: linear, arc, rising, descending, sweep, throw, or lock.
DEFENSE: block, parry, slip, duck, backstep, frame, or off-balance.
CONTACT POINT: fist, palm heel, forearm, elbow, knee, shin, shoulder, hip, or grip.
REACTION: head, shoulder, torso, knees, and footwork respond along the force line.
RECOVERY: limb retracts, support foot replants, guard returns, distance resets.
```

Style kernels:

| Style | Executable mechanics | Stability guardrail |
|---|---|---|
| Boxing | probing jab, straight cross, hook arc, slip/duck, guard recovery | use short combinations; retract every hand to guard |
| Muay Thai / kickboxing | forearm frame, clinch control, hip-driven knee, support-foot pivot, shin low kick | show support foot and post-contact recovery; no unsupported spinning |
| Kung fu / Wing Chun-like close range | centerline deflection, short bridge contact, palm strike, low kick, angle change | state which hand redirects which attack line; avoid vague “flowing” language |
| Karate | linear entry, rooted stance, straight strike, knife hand, front kick, clear kime pause | preserve pause and recovery; no endless speed chain |
| Taekwondo | bouncing range, support-foot pivot, high or spinning kick, landing orientation | one aerial action at a time; name landing foot and facing direction |
| Judo / wrestling / MMA | grip, off-balance, hip entry, leg block, throw arc, ground control | grip remains visible; state landing order and final positions |

Rules:

- Write attacker route first, defender solution second, counter third.
- A landed hit requires target reaction along the force line and attacker recoil/recovery.
- Use opponent waves or numbering for multi-person fights; only the current attacker performs a precise action.
- Preserve full-body geography for footwork and throws. Reserve CU/ECU for one decisive contact.
- Handheld shake cannot conceal bad choreography; use one primary camera move and a brief impact shake only.

Original internal example, compiled into the existing timeline structure:

```text
0-3秒，中景 lateral tracking。拳手B从 screen-right 向左前方压进，以左刺拳试探；拳手A右脚后撤半步，右前臂向外拨开拳路，双方距离缩短到肘膝范围。
3-7秒，A左手扣住B后颈形成单侧箍颈，髋部前送，右膝由下向上撞向B腹部护架；B双肘内收承受接触，上身后弓，鞋底在湿地面滑退半步，水花沿受力方向喷开。
7-10秒，B用左前臂顶开锁臂退出；A只完成一次外侧低扫踢，支撑脚转动、髋部带动胫骨接触B外侧大腿，随后立即收腿恢复护架。两人停在安全距离喘息。
```

#### Route 2: 武器格斗 / Weapon Combat

Lock the weapon before designing movement. A weapon has length, material, grip, edge/point direction, center of mass, inertia, recovery time, and collision behavior.

Silent ledger:

```text
WEAPON ID: type, length, material, color, wear, uniqueness.
HAND LOCK: one/two hands, dominant/off hand, grip position, visible hand change.
EDGE / POINT: blade edge, point, staff end, spear tip, shield face, or muzzle direction.
RANGE: close, middle, long, and safety gap.
WEIGHT / INERTIA: acceleration arc, braking, and recovery window.
CONTACT: weapon-to-weapon, weapon-to-armor, weapon-to-environment.
COUNTERFORCE: rebound, sliding bind, deflection, catch, disarm risk, or shield angle.
RECOVERY: weapon returns to guard, wrists/shoulders absorb shock, feet replant.
INVARIANTS: no disappearance, duplication, deformation, or unexplained hand switch.
```

Weapon kernels:

- Sword/blade: two-hand or one-hand grip, clear edge path, slash arc or thrust line, parry rebound, short riposte. A light trail never replaces the physical blade.
- Knife: close-body control, weapon wrist lock, short path, empty hand assigned to control. Avoid unreadable rapid stabbing.
- Spear/polearm: rear hand drives, front hand guides, point maintains range; do not compress it into short-stick motion.
- Staff: separated two-hand grip, torso-driven sweep, lift, end change, and continuous hand-to-shaft connection.
- Axe/hammer/heavy weapon: long wind-up, large inertia, heavy material result, long braking and whiff-punish window; never dagger speed.
- Shield: angled face redirects force into shoulder and feet; shield push has a visible step and recoil.
- Gun-fu: muzzle tracks only the current target, empty hand has one control job, shots have count and recoil, enemies are numbered.

Rules:

- Lock left/right hands and screen direction before parry, hand switch, or disarm. Any switch happens visibly.
- Weight controls cadence. Light weapons can redirect quickly; heavy weapons need longer wind-up and recovery.
- Bind collision to material feedback: metal ring/sparks, wood thud/fibers, shield bass vibration, stone scrape, water displacement.
- Blades do not require gore. Use cut fabric, severed leaves, armor sparks, dust, breath, and held reaction.
- Action video controls movement only; a storyboard controls shot order/axis and cannot override weapon design.

Original internal example:

```text
0-3秒，中近景，机位位于双方连线外侧。剑客A由 screen-left 向 screen-right 完成一次斜向下劈；肩、肘、腕依次传力，实体刀锋路径清晰。剑客B后撤右脚并抬剑形成交叉格挡，不同时进攻。
3-5秒，金属接触点保持在画面中央，短暂 slow motion；两把剑因碰撞向相反方向弹开，双方手腕和肩部出现反震。
5-8秒，剑客B依照动作参考A的转腕路径完成一次短促反击；剑客A侧身避开，刀锋从胸前安全距离掠过并割断一片前景竹叶。两人重新建立距离，武器回到警戒位。
```

#### Route 3: 能量招式 / Energy Technique

Energy must be grounded in visible body mechanics and world rules. It amplifies a force path; it does not replace body, contact, counterforce, or consequence.

Silent ledger:

```text
TECHNIQUE INTENT: which conflict state must change.
BODY SOURCE: feet, hips, torso, arms, breath, weapon, armor, or transformation core.
ENERGY SOURCE: body, environment, prop, element, machine core, or external formation.
CHARGE-UP: stance, gesture, breath, light, sound, and environmental response.
SHAPE / PATH: sphere, blade, beam, ring, flow, field, or coating; direction and speed.
RELEASE: when energy leaves the body or travels along body/weapon.
COLLISION / COUNTER: hit, block, deflect, absorb, cancel, interrupt, or miss.
MATERIAL RESPONSE: dust, water, cloth, metal, glass, plants, light, and air response.
RESIDUAL STATE: arcs, smoke, scorch, frost, cracked barrier, dim core, fatigue, recovery pose.
```

Technique kernels:

- Body reinforcement: local energy enhancement follows foot/hip/torso mechanics; it does not create weightless movement.
- Weapon infusion: lock the physical weapon first, then place energy along edge/point; physical contact and energy consequence occur in sequence.
- Projectile: use one primary projectile with source, path, target, collision, and residual state.
- Barrier/field: define center, boundary, facing, stress point, deformation, crack, slide, or failure cost.
- Element control: fire/water/wind/earth/ice/lightning affects nearby material, light, air, and sound along a stated direction.
- Teleport/high-speed move: state start, visible disappearance mechanism or motion trace, landing point, and new facing direction; prefer short dash or occlusion when possible.

Rules:

- One primary VFX event per beat. Charge, release, collision, and aftermath occur sequentially.
- Every technique has a cost or opening: charge time, exposed stance, decay, barrier crack, breathing disruption, overheating, or recovery pause.
- For energy-infused melee, state both physical contact and the energy response after contact.
- The opponent responds by dodge, block, deflect, absorb, interrupt, close distance, or exploit charge-up.
- Translate named inspiration into original function, shape, color, material response, and rhythm; do not depend on protected move names or franchise identifiers.
- Live-action priority: localized interactive light, air refraction, dust, water mist, cloth and material response; reduce UI, source-less particles, and continuous overexposure.

Original internal example:

```text
0-4秒，低机位中景。主角右脚向后踏实，重心降到髋部，右手收至肋侧；白蓝电弧只沿前臂缓慢聚集，衣摆和地面灰尘向身体内侧吸拢，表现蓄力而非立即爆炸。
4-8秒，对手从 screen-right 直线突进并挥出重拳；主角左前臂斜向格挡，使拳路偏离面部，接触处只出现一次短促白蓝闪光，双方肩部同时产生反作用。
8-12秒，主角借格挡形成的躯干旋转完成一次右掌反击，掌根接触对手胸前护甲；电能在实体接触后才向外扩散成三层递减冲击环。对手沿原突进路线反向滑退，主角前脚制动并恢复站姿；结尾只保留护甲表面游走的残余电弧。
```

Modules:

- Chase: pursuer distance changes, escape route visible.
- Escape: obstacle + exit route + crowd pressure.
- Close combat: hand/weapon contact point visible.
- Momentum Combat: body momentum carries into the next hit; no reset pose between strikes.
- Precision survival combat: target anatomy or weak point is named; each strike has visible effect.
- Giant struggle: human scale against giant joint, limb, claw, or shell.
- Creature Grapple: grip point on creature body, creature counterforce, slip/failure risk, recovery action.
- Rescue: danger line + target distance + time pressure.
- Falling: loss of balance -> grasp -> slip -> drop -> impact.
- Slide: surface friction, direction, endpoint.
- Side-scroller: subject centered, world scrolls.
- Hit and Run: strike then immediate exit direction.
- Prop fight: material and failure of prop.
- Team relay: A creates opening, B completes action.
- Air relay: arc, timing, catch point.
- Monster siege: threat directions and gaps.
- Crowd melee: main flow and protagonist anchor.
- Mounted chase: mount gait, rider grip point, foreground/background split, pursuer distance, obstacle, delayed blast or near miss.
- Gun-fu enemy chain: enemy numbers, exact order, gun hand/empty hand relation, bullet count, close-contact muzzle placement, recoil and corpse fall.
- Boss-to-live-action exchange: replace power, UI, boss, and loot with body, prop, space, material feedback, silence, and consequence; preserve route, contact, counterattack, charge-up, decisive contact, and aftermath.

Action problem fixes:

- If the fight feels like game CG, reduce VFX language and add weight, contact, recoil, breath, footwork, and recovery.
- If a character teleports between actions, state screen direction and the connecting step.
- If a weapon trail replaces the hit, name both the light trail and the physical strike target.
- If an action sequence feels one-sided, add opponent counterforce: block, shove, miss, bite/swing equivalent, interrupted route, recoil, or forced retreat.
- If a climax feels unearned, add charge-up: foot plant, two-hand grip, breath hold, silence drop, camera steadies, environment reacts.
- If the ending feels empty, add consequence: dropped prop, opened exit, stopped machine, silent room, debris settling, witness reaction, or visible evidence.
- If a rescue lacks tension, add the failure point: fingertip slip, rope strain, collapsing ledge, blocked route.
- If a multi-enemy fight becomes chaotic, number the enemies and time-box each kill or hit.
- If a chase loses comedy, separate foreground behavior from background threat: awkward or relaxed rider in front, dangerous horde behind.

## 14. Crowd Blocking

Crowd formula:

```text
main direction + counter direction + density + obstacle/congestion point + escape/flow route + protagonist relation
```

Modules:

- Crowd fleeing: one main escape direction, density increases at exit.
- Market lateral move: stalls create lanes, foreground occlusion.
- Tribal life: repeated small actions create culture; no random motion.
- Festival: circular flow around center symbol.
- Procession: ordered direction and rank separation.
- Beast migration: herd direction and dust wake.
- Crowd reaction: reaction spreads in waves.
- Protagonist against flow: protagonist vector opposes crowd.
- Chaos montage: fragments, but each fragment has direction.
- Ant-view overhead: top-down crowd routes readable.

## 15. Production Design

Design dimensions:

- settlement: layout, materials, water/food/fire logic, defensive logic.
- market: lanes, stalls, hanging fabric, trade goods, crowd routes.
- bedroom/interior: bed position, personal objects, practical light, class markers.
- costume: silhouette, material, wear, rank, color logic.
- weapons: material, craft level, damage pattern, handling sound.
- props: story function, use marks, scale.
- vehicles: propulsion logic, surface contact, cargo, wear.
- creature ecology: habitat, feeding marks, eggs/nests, tracks, waste, symbiosis.
- religion/symbols: repeated motifs, ritual objects, forbidden colors.
- craft materials: bone, bronze, clay, lacquer, rope, glass, woven fiber.
- life traces: stains, repaired seams, smoke marks, scratches, footprints.
- class difference: clean vs patched, polished vs handmade, symmetrical vs improvised.
- cultural mixing: explain why two cultures share materials or symbols.

Atompunk zombie city kit:

- era: parallel 1960s, cold-war space-age optimism collapsed by zombie outbreak.
- architecture: rounded domes, streamlined storefronts, beach villas, retro-future towers, neon signs, atomic-age interiors.
- contrast: sunny leisure color, sea sparkle, warm orange and sea-salt blue against blood, corpses, broken glass, abandoned cars.
- ruin traces: scattered newspapers, money, cocktails, beach props, hair salon tools, arcade tokens, cinema cups, drag-blood marks.
- lighting: harsh summer noon, hard-edged shadows, heat shimmer, dust in sun shafts, projection beam in cinema, blue-hour city blackout.
- story function: every location should express relaxing human life interrupted by collapse.

AI meta-stage and generated-scene kit:

- black void stage: pure black fantasy space, black absorbent cloth floor, no walls, no props, weak Rembrandt side light only on actors.
- actor boot state: character wakes like software starting, blinks once, scans left/right, body trembles on boot SFX.
- camera-as-sky: actors look upward into lens as if reading external instructions; keep all prompt text invisible.
- generated world loading: white 3D wireframe expands from feet, floor appears first, then walls/vehicles/lights/rain, then reflections and atmosphere.
- rain-night studio: deep blue industrial backlot, wet ground, metal warehouse, rolling door, cold wall lights, black car, red tail lights, puddle reflections, visible film equipment silhouettes.
- real-world creator space: night desk, laptop, warm desk lamp plus cool screen light, back-view creator, keyboard and Enter key as physical story trigger.
- story function: reveal that AI actors are performers responding to external prompt commands while still keeping cinematic reality intact.

Prompt kernel:

```text
PRODUCTION DESIGN: [space type], built from [materials], with [life traces], [class/culture markers], [story prop], all arranged to support [blocking/action].
```

## 16. Character Performance

Anchor layers:

- character anchor: face, age, body type, silhouette.
- face anchor: eyes, brows, mouth, skin marks, hairline.
- costume anchor: color, fabric, accessory, damage.
- voice anchor: breath, accent, volume, language rule.
- expression layer: micro-face state.
- action layer: body movement.
- rhythm layer: speed and hesitation.
- posture layer: weight, shoulders, center of gravity.
- reaction mode: freeze, retreat, attack, joke, deny, protect.
- flaw: pride, cowardice, obsession, guilt, innocence.
- arc: what changes by the end of the sequence.
- relationship: father/daughter, rival, protector, betrayer, fate link.

Robot LED-face performance:

- Face is not a morphing human face. It is a static LED/pixel display state.
- Each expression switch needs a short electronic SFX.
- Emotion is carried by body: posture, tempo, hesitation, hat gesture, gun handling, head turn, freeze, recoil.
- Keep display states consistent: cold blue = focused/cool, red = anger/combat, white = thinking/realization, symbol state = comedy.
- Do not animate facial muscles unless the robot design explicitly has them.

AI actor meta-performance:

- Actors may be aware of camera/sky as an external command source, but the screen/prompt text should not be visible unless the user requests readable UI.
- If characters read reference images or prompt instructions, express it through gaze, dialogue, timing, and reaction. Do not render floating subtitles.
- Keep comedy underplayed: small nose scratch, rain-wiping gesture, tired sigh, delayed look, restrained deadpan.
- When a character is "acting unconscious" or "pretending still", lock the body pose and allow only micro-mouth, one-eye peek, breath, or tiny eyelid motion.
- Clarify voice type: diegetic spoken line with lip movement, non-diegetic internal OS with no lip movement, or external creator voice.
- If a character secretly speaks while lying still, explicitly say it is real low-volume spoken dialogue from the mouth, not inner monologue and not narration.

Performance formula:

```text
FACE: [micro-expression].
BODY: [action].
RHYTHM: [tempo].
POSTURE: [weight].
REACTION: [how this character responds differently from others].
```

Example:

```text
FACE: deadpan face, eyes fixed forward.
BODY: fast purposeful walk through panicking crowd.
RHYTHM: no hesitation.
REACTION: everyone backs away, she cuts straight toward the sound.
```

### Actor Emotion & Physical Performance Engine v3

Purpose: translate user feelings such as "压迫", "疯癫", "冷峻", "崩溃", "宿命", "有电影感", or "like a famous scene feeling" into playable actor behavior and model-readable image changes.

Silent performance ledger:

```text
OBJECTIVE: what the character wants right now.
OBSTACLE: what blocks the objective.
TACTIC: request / threaten / seduce / control / hide / deny / escape / bargain / surrender.
BEAT REVERSAL: what changes the tactic.
PUBLIC MASK: what the character tries to show others.
PRIVATE LEAK: what the body accidentally reveals.
FACE LAYER: eyes, brow, jaw, mouth corners, blink rate, tears, gaze target.
BREATH LAYER: held breath, short inhale, swallowed breath, broken exhale, breath recovery.
BODY LAYER: neck, shoulders, hands, torso, hips, knees, feet, center of gravity.
HAND BEHAVIOR: grip, release, hide, touch, tremble, wipe, cover, point, fail to grip.
EYE-LINE BEHAVIOR: lock, avoid, search, check exit, return to object, look through person.
WEIGHT SHIFT: lean forward, step back, freeze, collapse, brace, sink, stand taller.
RHYTHM LAYER: pause, interruption, delayed response, sudden acceleration, freeze.
MASK VS LEAK: what the character tries to show vs what the body reveals.
REACTION OWNER: whose reaction teaches the audience what the event means.
```

Rules:

- Do not write only "he is sad", "she is angry", "he is terrified". Convert emotion into visible face, breath, body, rhythm, and silence.
- Emotion needs a trigger: a seen object, heard sound, line of dialogue, blocked exit, touch, memory clue, or spatial reveal.
- Strong emotion can be still. A held face, delayed blink, swallowed breath, or frozen hand can carry more weight than a large gesture.
- Separate mask and leak: `calm face + fingers tighten around the cup`, `polite smile + shoulders stop moving`, `deadpan face + fast purposeful walk`.
- Dialogue performance is action. State whether the character attacks, deflects, begs, controls, withholds, or tests the other person.
- Use reaction cuts when the emotion's meaning matters more than the event itself.
- For Seedance, stage emotional change in visible increments: trigger -> micro-reaction -> body leak -> decision or collapse.
- If the user asks for a "feeling", do not output a psychology essay. Compile it into 目标、阻碍、策略、表面控制、真实泄露和节拍反转.
- Strong performance often uses contradiction: calm face + violent hand, polite smile + frozen shoulders, soft voice + controlling eyeline, fast walk + deadpan face.
- A beat reversal must have a visible trigger: new sound, object reveal, touch, line, blocked exit, eye contact, or background movement.

Feeling-to-performance quick map:

| Feeling | Performance translation |
|---|---|
| oppressive | reduced movement, low voice, still seated body, other character leans forward or lowers gaze |
| dread | eyes check off-screen space, breath shortens, shoulders rise, hands search for exit/tool |
| grief | eyes avoid the object, jaw holds, breath breaks, shoulders lose height, hand remains on prop |
| rage under control | calm face, fixed stare, jaw tightens, fingers whiten on object, voice slows |
| panic | gaze jumps, feet misstep, hands fail to grip cleanly, breath becomes audible |
| cold authority | minimal face change, slow blinking, controlled posture, silence before response |
| madness / fracture | rhythm breaks, gaze misaligns with action, laugh/breath arrives late, body over-precise or too still |
| destiny / fate | eyes lock to unseen direction, body freezes before explanation, environment or sound changes first |
| shame | gaze avoids the witness, mouth opens then closes, hand hides object/body mark, weight shifts backward |
| suspicion | eyes scan mismatch, body stays polite, hand protects pocket/door/object, response arrives late |
| seduction/control | movement slows, distance narrows deliberately, gaze holds longer than normal, object is touched as leverage |
| heroic resolve | breath steadies, feet plant wider, shoulders square, hand re-grips prop, gaze locks toward route |
| betrayal realization | blink delay, face stops moving, breath drops out, eyes return to the betrayer/object |
| dissociation | face is too blank, body obeys slowly, gaze passes through people, sound narrows subjectively |

Prompt kernels:

```text
PERFORMANCE INTENT: [character] wants [objective] but [obstacle] blocks it; tactic shifts from [first tactic] to [new tactic] when [beat reversal] occurs.
MASK VS LEAK: face shows [controlled mask], but body leaks [hand/breath/shoulder/feet behavior].
EMOTION TIMELINE: trigger [visual/sound/line] -> micro face change -> breath/body leak -> decision/collapse/recovery.
PHYSICAL PERFORMANCE: public mask [shown behavior], private leak [accidental body cue], eyeline [target], hand behavior [action], weight shift [direction], reaction owner [who teaches the audience].
```

## 17. Creature, Disaster, Comedy, Transformation

Creature reveal orders:

- Spielberg chain: sound -> reaction -> partial body -> environmental effect -> full reveal.
- Dune scale reveal: tiny human -> landscape shift -> slow tilt/pull-back -> impossible size.
- Partial puzzle: claw, breath, shadow, footprint, eye, only then body.
- Mountain-is-body: landscape detail moves, audience realizes it is alive.
- Disaster countdown: animals react, dust line, ground tremor, crowd recognition, impact.

Disaster escalation:

- omen -> first physical change -> individual reaction -> crowd wave -> blocked exit -> structural failure -> aftermath detail.

Comedy action:

- play action seriously; comedy comes from result mismatch, delayed reaction, object failure, timing reversal.

Transformation:

- identity before change -> trigger contact -> local body/object change -> energy/material spread -> full assembly -> cost/reaction -> final pose.

## 18. Model-Specific Compiler

Model specs change. Verify live docs when precision matters.

| Model | Segment duration | Context memory | Long take | Hard cuts | Text/dialogue | Complex action | Consistency | Prompt length | Advice |
|---|---|---|---|---|---|---|---|---|---|
| Seedance | hard rule here: <=15s | stateless | good if one action chain | separate segments | avoid readable text dependency | moderate; split contact-heavy action | repeat face/costume/silhouette/color every segment | <=10000 chars; often 800-1800 Chinese chars | independent complete segment; STYLE LOCK first; ending state |
| 可灵 / Kling | often 3-15s depending mode | limited | good short dynamic shots | separate clips | simple text only | good dynamic motion, simplify multi-person | use image refs and repeated anchors | 400-1200 Chinese chars | subject + action + camera + environment + ending frame |
| Veo | commonly 8s in API surfaces; varies | better inside clip | strong cinematic short takes | one prompt per shot unless sequence supported | audio/dialogue depends surface | strong physical causality | repeat anchors, use first/last frame if available | 600-1600 Chinese chars | scene + style + camera + action + ambience + time progression |
| Runway | Gen-4 commonly 5s or 10s | clip-level | short controlled shots | one prompt per shot | readable text risky | moderate; one main motion | strong with source image | 1-3 concise sentences | subject lock, camera verb, motion verb |
| Pika | short expressive clip | clip-level | short effects | one prompt per beat | avoid critical text | simple motion/effects | image anchor recommended | 1-2 concise sentences | one subject, one effect, stable background |
| Sora | public surfaces vary | stronger temporal coherence | strong with causality | can describe sequences but keep cut reasons clear | varies | strong but contacts need constraints | recurring anchors and state continuity | 800-2200 Chinese chars | temporal progression, physics, spatial layout, unchanged constraints |
| Midjourney Video | 5s image-to-video unit | image-based | short animation | not multi-shot editor | avoid text dependency | weak for multi-step action | strong if still image is strong | very short motion phrase | what moves, what stays fixed, camera motion, intensity |

Seedance compiler:

```text
基础风格锁定 -> 角色/场景/素材锁定 -> 单段时长 <=15s -> 一条连续动作链 -> 运镜 -> 空间关系 -> 光线/色彩 -> 声音确认 -> 结尾状态。
```

Seedance cut/segment compiler:

```text
Pack storyboard beats into the fewest readable Seedance prompt blocks. Keep continuous action, same speaker, and same-space story inside one `5-15s` segment. Split only when the scene/location changes, shot scale or camera setup changes enough to confuse the model, primary character/speaker changes, a separate action chain begins, a time state changes, or the previous causal action unit has ended. In one Seedance prompt, use one continuous shot or a short time-axis with clear internal markers; do not ask the model to execute a dense unrelated edited sequence.
```

Repair matrix:

- character drift: repeat visual anchor, face/costume markers, silhouette, color.
- action mush: reduce to one causal chain, name contact points.
- camera ignored: put camera movement near front, use English term.
- scale unclear: add human reference and camera pull-back.
- extra events: remove abstract prose, use one-beat-one-info, then pack compatible beats into a readable 5-15s segment.
- bad cut continuity: add ending state and next-shot starting state.
- too much text: move analysis outside prompt; keep production instructions only.

Seedance Stability Gate v2:

Run this gate silently before delivery. It is a prompt-side failure prevention pass, not a visible analysis section.

| Risk | Silent check | Prompt-side fix |
|---|---|---|
| cut drift | after every cut, are positions, facing direction, camera side, and starting state clear? | re-anchor screen-left/right, depth plane, camera side, and first visible body state |
| too many tracked subjects | are more than 3 individual subjects doing specific actions? | track the acting pair or trio; turn the crowd into one mass with a flow direction |
| off-screen state change | does something change while invisible and then become important? | reveal the change on camera first, or make the off-screen sound/reaction lead into the reveal |
| exit/re-entry confusion | does a subject leave and re-enter the same continuous shot? | split the beat, or keep exit visible and make re-entry simple with a clear route |
| multi-motion overload | are push, pan, rise, handheld, focus pull, and orbit stacked together? | keep one primary camera move per shot/time beat; if needed, sequence moves with timestamps |
| weak geometry | door, hallway, stairs, vehicle, crowd, machine, or furniture route is under-specified | state camera start position, fixed objects, travel direction, obstacle, and destination |
| source-frame invention | required prop/location/action is absent from the reference image or keyframe | state the absence as intentional: `[object] is not visible in @Image, it appears when...` |
| adjacent-object drift | one object moves and a nearby object should not | name invariants: `[fixed object] stays attached/still; only [moving object] moves` |
| reflection/text risk | mirror, water reflection, screen text, signs, dense UI, or subtitles carry key information | use a dedicated shot/post overlay; keep in-scene text short, large, and non-critical |
| duplicate identity risk | same character appears as clone, mirror self, memory self, or time double | name each instance as a separate role with separate wardrobe/time-state anchors |
| reference-audio leakage | reference audio is only a beat guide but may be heard in output | write a clear no-output rule; use simplified beat/SFX guide, stems, or final audio replacement; keep final sound layer explicit |
| audio-style drift | music mood pushes the scene toward dance, game-like combat, close-up emotion, or long lyrical hold against the story | re-state scene function, action route, contact points, shot purpose, and ending state; use fewer music-driven beats |
| continuation without evidence | next-part prompt assumes the previous planned ending happened | require accepted clip, final frame, or exact visible-end description; begin from observed state |
| completed-beat replay | the prompt repeats an action already shown in accepted footage | mark it already happened; write it only as context, not as current action |
| reserved-future leakage | the prompt performs a later beat early | move the beat to reserved future and add a stop-before endpoint |
| budget overload | identity, bold motion, dense scene, readable text, and dialogue are all primary | choose one primary spend, one secondary spend, then split or simplify the rest |
| prompt overload | final prompt has several scenes, actions, or effects in one segment | split into independent <=15s segments; keep STYLE LOCK, character/scene lock, one action chain, and ending state |

Gate kernel:

```text
SEEDANCE STABILITY: one primary camera move; no more than three tracked subjects; after each cut re-anchor screen direction and starting state; fixed objects stay fixed; off-screen changes are revealed before use; high-risk reflection/text/crowd/clone content is simplified or isolated.
```

## Practical Problem-Solution Engine

This section distills the provided 2026.03.15 prompt/problem examples into reusable repair rules. Use it when the user asks for high-detail transformation, mecha/tokusatsu, reference-image identity, or when a prompt is too long or unstable.

### Character identity lock from reference images

Use when a human face must remain identical across transformation, armor, injury, or action.

```text
FACE LOCK: reference image is the only identity source. Preserve facial proportions, bone structure, jaw geometry, hairline, hairstyle, injuries, bruises, blood stains, bandages, and expression baseline. No beautification, no idolization, no face reshaping.
```

Rules:

- Write what must stay the same: face, jaw, hair, wounds, costume marks.
- Write what may change: armor, light, damage, supernatural markings.
- If a tattoo/totem/reference painting is provided only for markings, explicitly say it must not influence facial identity.
- For transformation, state that the pre-transformation and post-transformation face share the same bone structure.
- Avoid vague "same person"; specify the stable facial geometry.

### 15-second battle-damaged transformation engine

Use for dark tokusatsu, creature armor, mecha armor, magical girl bank, bio-mechanical upgrade, or body-horror transformation.

Core structure:

| Time | Beat | Required content |
|---|---|---|
| 0-3s | Stare / trigger preparation | low emotional state, gaze locks device/body part, hand raises, breath and micro camera float |
| 3-6s | Activation | spoken trigger or silent press, core cracks, light leaks, air collapses, pulse wave, hair/fabric disturbance |
| 6-9s | Rupture / tearing | clothing burns or tears, skin/armor cracks, fluid/light threads, fragments suspend or recoil, camera shake/focus snap |
| 9-12s | Growth / assembly | new matter pushes out, plates collide, mask spreads, eyes/visor light in uneven order, malfunction detail |
| 12-15s | Completion / aftermath | final silhouette, remaining wound or crack, glow drops, one lingering unstable light, final pull-back or orbit |

Camera grammar:

- One continuous take when the model can handle it; otherwise split into 2-3 independent segments.
- Opening may use low angle from left 30 degrees, waist-up or half-body.
- Slow orbit from side to front during transformation, then to right-side high angle or slow pull-back after completion.
- Add tiny handheld breathing movement for live-action presence.
- Use momentary impact shake only at activation or rupture, then snap back into focus.

Tone rules:

- Dark transformation is not heroic upgrade language. Keep fatigue, pain, pressure, incomplete armor, damaged surface, low saturation.
- Avoid "glorious explosion", "bright triumph", "perfect shiny suit" unless the user asks.
- Strong ending: no extra speech, no victory pose, no explosion; the changed body stands in smoke/wind with one unstable detail still pulsing.

VFX detail vocabulary:

- crystal core cracks, dark red/blue light leaks, air collapses inward, transparent pulse wave spirals outward.
- eye glow creates lens flare, skin cracks 1.5cm, internal orange pulse opens and closes with heartbeat.
- wet biomaterial extrudes, iridescent surface crawls, tissue strands pull then recoil.
- armor plates collide and leave burn-like bite marks, chest plates open/close with heartbeats.
- compound eyes assemble unevenly, individual units flicker, one defective unit hisses every few seconds.
- glowing cracks breathe with the body; brightness drops after completion except one wound.

### Mecha and power-armor prompt repair

Use for Pacific-scale mecha, cyberpunk armor, tactical vest, arm controller, powered suit, heavy weapon, or boss fight.

Rules:

- Use owned/generated reference images for character, armor, weapon, or creature instead of depending on copyrighted design names.
- Translate inspiration names into original descriptors: heavy industrial mecha, matte titanium, worn paint, oil in joints, HUD glow, contact shadows.
- State mechanical scale by ratio: exoskeleton is 50 times larger than pilot, or armor parts unfold from back/arms.
- Add material logic: titanium alloy, matte black coating, scratches, oil stains, exposed joints, hot orange core, red HUD glass.
- For aerial or falling mecha, add inertia and camera speed matching: falling subject catches camera, camera matches speed, distance changes with aerodynamics.
- For water/ground impact, describe the force result: ring-shaped water wall, white foam, debris, camera water drops, delayed bass impact.

### Overlong prompt and model-collapse repair

Symptoms:

- model ignores instructions
- character face drifts
- action becomes mushy
- prompt exceeds mobile/app limits
- one-take sequence collapses
- generated result looks like game CG instead of live action

Repairs:

- Split into independent clips: setup, transformation/action, final pose/result.
- Move analysis out of the prompt; keep only production instructions in the final model prompt.
- Preserve only core anchors in every segment: STYLE LOCK, face/costume lock, scene lock, camera, one action chain, ending state.
- Replace long IP references with concrete visual descriptors.
- Reduce simultaneous effects; keep one primary VFX event per 2-3 seconds.
- If mobile prompt length is too short, use web version or shorter prompts; do not pretend a dense 15s transformation will be stable in a tiny prompt box.
- If the model is currently unstable, prefer generated reference images plus shorter clips and post-editing rather than one giant prompt.

### AI actor meta-scene repair

Use for prompts where characters are AI actors, read external instructions, load into a generated scene, or complain about prompt failures.

Risks and repairs:

- Actors vanish during wireframe loading: state that actors remain fully visible, unhidden, unoccluded, and in the same standing positions while the world loads around them.
- Scene loading becomes a hard cut: require one continuous shot, no hard cut, no black transition, environment appears in ordered layers.
- Prompt/reference text appears on screen: state that sky information is invisible and communicated only through character gaze and spoken dialogue.
- Wide-angle comedy deforms faces too much: allow mild 16mm close distortion but forbid fisheye, edge bending, and identity drift.
- Costume hot-swap redraws the face: stage the outfit change while the actors turn to side/back view; forbid new face information during the change.
- Real-world creator shot invents readable UI: allow blurred interface only; do not depend on exact screen text.
- Whispered joke becomes inner OS: explicitly label it as diegetic low-volume spoken dialogue with tiny lip movement.
- Pose-locked callback moves too much: lock body pose, hand position, head angle, costume, and environment; allow only eyes/lips/breath.

Reusable meta-scene segment shapes:

- Black-space boot-up: close side face -> front face scan -> full-body standing -> top-down camera-as-sky.
- Second actor drop-in: feet foreground -> actor falls into empty black space -> focus transfer -> painful wake-up -> first spoken joke.
- External prompt wait: two-shot looking at camera/sky -> keyboard typing sound -> small bored gestures -> no visible text.
- Scene generation: Enter sound -> white wireframe from feet -> floor/walls/props/lights/rain load in order -> actors remain centered.
- Reference-reading comedy: close two-shot looking up -> one character misreads reference -> partner corrects -> restrained embarrassment.
- Creator cutaway: back-view desk -> tired line -> hand presses Enter or resumes typing -> no readable UI.

### Copyright and reference hygiene

- Do not require direct copyrighted character or franchise replication unless the user owns/provides the reference and explicitly requests that workflow.
- Safer default: convert named references into style mechanics, material, lighting, camera, and emotional descriptors.
- Encourage original AI-generated reference images for armor, weapons, mecha, monsters, and costume boards.
- When using a reference only for pose, costume, or marking, state what must be borrowed and what must not be borrowed.

## 19. Output Format

Default full format:

```text
For Seedance or any output using Chinese section headings, do not output standalone 【画面结构与构图】, 【焦点路径】, or 【结尾状态】 by default. Use:
【运镜与时间轴】: each time beat includes duration rationale, shot size, camera position, movement, screen-left/right, foreground/midground/background, composition, focus path, action timing, marker, sound cue, cut reason, and ending state.
For each time beat, choose duration by function and readability: impact flashes can be under 1s, single information/dialogue beats often need 1-2s, spatial scans and multi-person posture often need 2-3s, emotional/atmosphere holds often need 3-5s, and immersive long-take or monologue beats can need 5-8s or longer only when internal markers keep the shot alive.

## 导演分析
- 故事核心:
- 角色/关系/弧光:
- 场景/世界观:
- 叙事节拍:
- 视觉锚定:
- 导演框架:
- 摄影风格:
- 模型策略:

## 连续分镜提示词

### 第01段｜8-15秒｜[场景功能]
【基础风格】
【角色/场景/素材锁定】
【运镜与时间轴】
【声音设计】
【画面限制】

## 连续性检查
- 角色连续:
- 场景连续:
- 动作因果:
- 空间方向:
- 声音绑定:
- 模型限制:
```

Compact prompt block:

```text
第01段｜8-15秒｜[场景功能]
【基础风格】
【角色/场景/素材锁定】
【运镜与时间轴】
【声音设计】
【画面限制】
```

Final checklist:

- `【基础风格】` appears first in every independent segment, repeats the project-level camera/lens/color/texture baseline, and adds the scene-specific lighting/atmosphere/material response.
- `【角色/场景/素材锁定】` merges reference usage, character identity, scene identity, props, color cards, and voice/audio anchors; default output does not split them into separate reference/scene/character sections.
- Every @image/@video/@audio reference has a role, dimension lock, and short locked name; visible output states what each reference controls, and states what it does not control only when ambiguity or drift risk makes that useful.
- `【运镜与时间轴】` uses locked names instead of repeatedly calling @references unless a new reference first appears in that beat.
- If reference audio exists, the prompt states whether it is final BGM, silent beat guide, SFX guide, ambience bed, or voice anchor; silent guide audio is explicitly not output as BGM, and later sound wording does not contradict it.
- If a painter, movement, or art style is referenced, it is translated into visible line, color, composition, texture, light, mood, and use case inside `【基础风格】`.
- Segment duration fits target model; for Seedance, compatible beats are packed into 5-15s blocks instead of one prompt per storyboard shot.
- Seedance segment is independent and <=15s.
- Seedance segmentation follows packing logic: do not output one prompt per storyboard shot; pack compatible beats into 5-15s blocks, and split only at strong scene, camera-readability, character/speaker, time-state, or completed-action boundaries.
- Continuation starts from accepted footage, an accepted final frame, or an exact visible-end description; planned endings are not treated as actual endings.
- Completed beats are not replayed, current segment beats are executable, and reserved future beats do not appear early.
- Prompt budget has one primary spend and at most one secondary spend; overloaded identity/action/crowd/dialogue/text demands are simplified or split.
- Retake advice, if requested, uses keep / post / edit-one-layer / re-roll / rewrite and changes one variable at a time unless the strategy itself must change.
- Adjacent Seedance segments have a clear boundary contrast: the last beat of one and first beat of the next do not repeat the same subject, shot scale, and composition; no forced mask/wipe transition is used unless story-motivated.
- One storyboard beat has one primary information unit; one Seedance segment may pack several compatible beats.
- Camera grammar and movement are explicit.
- Action chain is causal and spatial.
- Martial action selects one primary route among 空手格斗、武器格斗、能量招式, with at most one secondary route for a hybrid fight.
- Martial attack, defense, contact, recoil, recovery, weapon continuity, charge-up, energy collision, and aftermath are bound to exact `【运镜与时间轴】` beats; no default standalone fight/action/technique section appears.
- Unarmed combat uses attack-response and recovery; weapon combat locks hands, direction, weight, collision material, and invariants; energy techniques preserve body source, charge-up, collision/counterforce, material response, cost, and residual state.
- CAMERA / TIME AXIS integrates duration rationale, screen-left/right, foreground/midground/background, subject/object positions, focus path, movement, marker, sound cue, cut reason, and ending state.
- Crowd/background continuity is explicit when present: background extras and blurred crowds do not disappear between beats, wide shots, or segments unless the prompt states how they leave, disperse, are occluded, or are cropped out.
- Timeline beat durations match shot function, information density, motion intensity, dialogue/action readability, emotional hold, sound bridge, and target-model limits.
- Important motion is decomposed into body-part mechanics, weight shift, contact/failure, recoil, and recovery.
- Lighting has source, direction, intensity, shadow, material reaction.
- Famous-scene feeling, if mentioned, is translated into original scene grammar; no protected characters, dialogue, costumes, exact staging, shot order, or franchise identifiers are copied.
- Actor emotion is visible as 目标、阻碍、策略、表面控制、真实泄露、节拍反转、视线、手部行为、重心变化、面部、呼吸和身体。
- Visual impact or reversal changes knowledge, power, danger, scale, conflict state, or consequence.
- Montage, if used, changes time, place, emotion, evidence, pressure, or consequence and uses visual rhyme, sound bridge, action match, color match, or object match.
- Genre feeling is compiled through a mechanism pack such as horror threshold, crime power, action route, disaster scale, sci-fi perception, romance memory, animation impact, or absurd comedy.
- Cut reason is stated.
- Sound confirms action or leads transition.
- If a reference audio/video voice is used, voice tone is locked separately from face/body/dialogue and repeated in each independent segment where the character or narrator speaks.
- Ending state is named inside the final time beat and sets up the next shot.
