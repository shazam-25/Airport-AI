class MultiCameraManager:
    def __init__(self, pipelines):
        self.pipelines = pipelines

    def run(self):
        while True:
            for pipeline in self.pipelines:
                pipeline.process_frame()

# if __name__ == "__main__":
#     pipelines = []
#     for config in CAMERAS:
#         pipelines.append(
#             CameraPipeline(
#                 camera_id=config["camera_id"],
#                 source=config["source"],
#                 tracker=tracker,
#                 turnaround=turnaround,
#                 ppe=ppe,
#                 fod=fod,
#                 repository=respositoy
#             )
#         )