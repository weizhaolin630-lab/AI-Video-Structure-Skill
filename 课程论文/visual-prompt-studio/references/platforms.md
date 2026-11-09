# 平台适配

只在用户指定平台或需要执行时查对应行。分别记录应用入口和模型。第三方多模型入口的参考图标记、设置与直连 API 可能不同，使用前以该入口为准。型号与入口会更新，需核对具体尺寸、时长、参考上限、接口参数与可用功能。只编写提示词时，可以在正文外给出用户要设置的目标规格。

| 平台 | 写提示词时的差异 | 官方依据 |
| --- | --- | --- |
| Midjourney | 优先描述画面内容和效果，保留用户已给的有效参数。将已确认的画幅等参数放在末尾，或单列界面设置。用户要求减弱默认风格时用 Raw 或调整 Stylize。风格参考放在对应的参考类型。指定画中文字时用半角双引号括住原文 | [参数表](https://docs.midjourney.com/hc/en-us/articles/32859204029709-Parameter-List) · [文字生成](https://docs.midjourney.com/hc/en-us/articles/32502277092109-Text-Generation) |
| GPT Image | 描述主体、构图及约束。改图先写改动与保留项。尺寸与渲染质量以型号支持的界面或 API 设置为准。有精确版式时明确位置、留白和逐字内容 | [OpenAI 图像提示指南](https://developers.openai.com/api/docs/guides/image-prompting) |
| Nano Banana | 支持多轮改图的入口可沿用同一参考，每轮聚焦一个改动。多图时按编号明确外观、构图、材质等作用。尺寸和画幅放在入口的设置处 | [Gemini 图片生成指南](https://ai.google.dev/gemini-api/docs/image-generation) |
| Seedream（静态图片） | 即梦或其他入口选定 Seedream 后，用用户语言写清主体、版面关系、指定文字与参考角色。需要一套图时说明共享的主体造型和每张的差异。圈选等能力按入口支持情况使用 | [Seedream 5.0 Pro 官方介绍](https://seed.bytedance.com/en/blog/beyond-generation-it-understands-design-introducing-seedream-5-0-pro) |
| Seedance | 适配视频。明确哪份参考定外观、首帧、运镜或声音，按时间写可见事件。先核对用户实际入口支持的时长及参考类型。目标超出当前入口时保留完整分镜，另列可执行的分段或延长路径 | [Seedance 2.0 技术报告](https://arxiv.org/abs/2604.14148) · [Seedance 2.5 官方介绍](https://seed.bytedance.com/en/blog/one-take-creation-flexible-referencing-introducing-seedance-2-5) |

## 交付示例

- 输入「图片，老唱片封面，昏暗一点，标题是『回声』」。可交付「方形唱片封面。暗棕木桌上的黑胶居中，侧上方一束窄暖光擦过唱片细纹，背景留深色层次。封面上方留空，只在上方居中写『回声』，使用米白色简洁标题字。」
- 输入「Midjourney，3:2 的窗边咖啡，像街拍，少一点默认美化」。可交付「街头纪实照片。咖啡杯放在旧木窗台，平视近景，阴天窗光照亮杯沿，远处街景略虚，保留木面划痕和自然暗部。 --ar 3:2 --raw」
- 输入「视频，雨夜骑士向右走，镜头跟着他，无对白」。可交付「雨夜，深色斗篷骑士始终向画面右侧走。镜头在侧面等速并行跟拍，保持距离。车灯从侧后方照亮雨丝，骑士踏过积水时溅起水花，最后向右走入暗处。无对白。」此例保留用户的声音约束，雨声和配乐由用户偏好决定。
