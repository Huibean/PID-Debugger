class CommandTranslator():
    header = "aa55"
    footer = "0d"

    @staticmethod
    def convert_hex_string(command, positions_buffer, rotations_buffer):
        print("处理坐标: ", positions_buffer)
        pack_position = (0, 0, 0)
        pack_rotation = (0, 0, 0)

        command_hex = command
        positions_hex = ''
        check_hex = int(command_hex, base=16)

        range_size = 10
        data_size = len(positions_buffer)

        for index in range(range_size):
            if index + 1 <= data_size:
                position = positions_buffer[index + 1]
                rotation = rotations_buffer[index + 1]
                print("Roll: {0}, Pitch: {1}, Yaw: {2} \ radian".format(*rotation))
            else:
                position = pack_position
                rotation = pack_rotation

            x = position[0]
            y = position[2]
            z = position[1]
            yaw = rotation[2]

            if index + 1 <= data_size:
                print(position)
                print("x: {0} y: {1} z: {2} yaw: {3}".format(x, y, z, yaw))

            x = format(int(x * 100 + 500), "04x")
            y = format(int(y * 100 + 500), "04x")
            z = format(int(z * 100 + 500), "04x")

            yaw = format(int((yaw + 360) * 100), "04x")

            position_hex = x + y + z + yaw
            positions_hex += position_hex

            for item in [x, y, z, yaw]:
                check_hex += int(item[0:2], base=16)
                check_hex += int(item[2:4], base=16)

        check_hex = format(check_hex, "04x")[-2:]
        print("校验码: %s"%check_hex)
        
        hex_string = CommandTranslator.header + command_hex + positions_hex + check_hex + CommandTranslator.footer

        print("生成数据: %s"%hex_string)
        return bytearray.fromhex(hex_string)
