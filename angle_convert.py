import math
class AngleConvert():

    @staticmethod
    def quaternion_to_euler(q, type="angle"):
        qx, qy, qz, qw = q
        roll = math.atan2(2*(qw*qx + qy*qz), 1 - 2*(qx ** 2  + qy ** 2))
        print("Roll: %s"%roll)

        t2 = 2*(qw*qy - qz*qx)
        #  if t2 > 1:
            #  t2 = 1.0
        #  elif t2 < -1:
            #  t2 = -1.0

        pitch = math.asin(t2)
        print("Pitch: %s"%pitch)

        yaw = math.atan2(2*(qw*qz + qx*qy), 1 - 2*(qy ** 2 + qz ** 2))
        print("Yaw: %s"%yaw)

        if type == "radian":
            return [roll, pitch, yaw]
        else:
            return [ i * 180 / math.pi for i in [roll, pitch, yaw]]


result = AngleConvert.quaternion_to_euler((0.49846121668815613, 0.5050917863845825, 0.5173382759094238, 0.4783095121383667))
print(result)
