from ok import TriggerTask

liveEndText = "直播已结束"
claimText = "立即领取"


class AutoClaim(TriggerTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "自动领取"
        self.found_count = 0

    def run(self):
        self.log_info(self.hwnd_title)
        boxByFeature = self.find_one(feature_name="coupon", vertical_variance=5)
        if boxByFeature:
            self.found_count += 1
            self.log_info(f"Target button found by feature({self.found_count})", True)
            self.click_box(boxByFeature)
        else:
            ocrBoxes = self.ocr(match=[liveEndText, claimText])
            for ocrBox in ocrBoxes:
                if ocrBox.name == liveEndText:
                    self.log_info(liveEndText, True)
                elif ocrBox.name == claimText:
                    self.found_count += 1
                    self.log_info(
                        f"Target button found by ocr({self.found_count})", True
                    )
                    self.click_box(ocrBox)
        self.sleep(10)
