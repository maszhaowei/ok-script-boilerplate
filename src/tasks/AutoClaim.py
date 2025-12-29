from ok import TriggerTask

liveEndText = "直播已结束"
claimText = "立即领取"


class AutoClaim(TriggerTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "自动领取"
        self.click_count = 0

    def run(self):
        self.log_info("finding...")
        boxByFeature = self.find_one(feature_name="coupon", vertical_variance=5)
        if boxByFeature:
            self.click_box(boxByFeature)
            self.click_count += 1
            self.log_info(f"Target button found by feature({self.click_count})", True)
        else:
            ocrBoxes = self.ocr(match=[liveEndText, claimText])
            for ocrBox in ocrBoxes:
                if ocrBox.name == liveEndText:
                    self.log_info(liveEndText, True)
                    break
                elif ocrBox.name == claimText:
                    self.click_box(ocrBox)
                    self.click_count += 1
                    self.log_info(
                        f"Target button found by ocr({self.click_count})", True
                    )
                    break
        self.sleep(10)
