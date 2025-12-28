from ok import TriggerTask


class AutoClaim(TriggerTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "自动领取"
        self.click_count = 0

    def run(self):
        self.log_info("finding...")
        liveEnd = self.ocr(match="直播已结束")
        if len(liveEnd) > 0:
            self.log_info("直播已结束", True)
        feature = self.find_one(feature_name="coupon", vertical_variance=5)
        if feature:
            self.click_box(feature)
            self.click_count += 1
            self.log_info(f"Target button found by feature({self.click_count})", True)
        else:
            ocr_boxes = self.ocr(match="立即领取")
            if len(ocr_boxes) > 0:
                self.click_box(ocr_boxes[0])
                self.click_count += 1
                self.log_info(f"Target button found by ocr({self.click_count})", True)
        self.sleep(10)
