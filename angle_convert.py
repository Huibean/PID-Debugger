import math
class AngleConvert():

    @staticmethod
    def quaternion_to_euler(q, type="angle"):
        print("转换四元数: ", q)
        qx, qy, qz, qw = q

        t0 = 2*(qw*qx + qy*qz)
        t1 = 1 - 2*(qx ** 2  + qy ** 2)

        roll = math.atan2(t0, t1)

        t2 = 2*(qw*qy - qz*qx)
        if t2 > 1:
            t2 = 1.0
        elif t2 < -1:
            t2 = -1.0
        pitch = math.asin(t2)

        t3 = 2*(qw*qz + qx*qy)
        t4 = 1 - 2*(qy ** 2 + qz ** 2)
        yaw = math.atan2(t3, t4)

        if type == "radian":
            result = [roll, pitch, yaw]
            print("Roll: {0}, Pitch: {1}, Yaw: {2} \ radian".format(*result))
        else:
            result = [ i * 180 / math.pi for i in [roll, pitch, yaw]]
            print("Roll: {0}, Pitch: {1}, Yaw: {2}".format(*result))
        return result
