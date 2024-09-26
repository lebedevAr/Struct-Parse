from struc2 import Struct, Tag, LittleEndian


class TestProtocol:
    @staticmethod
    def parse(byte_string):
        class Blank(Struct):
            num_pack: Tag[int, 'u8']
            type_message: Tag[int, 'u8']
            imei: Tag[str, 15, 'cstring']
            datetime: Tag[int, LittleEndian, 'u32']
            lat: Tag[float, LittleEndian, "f32"]
            lon: Tag[float, LittleEndian, "f32"]

        class BlankExtended(Struct):
            num_pack: Tag[int, 'u8']
            type_message: Tag[int, 'u8']
            imei: Tag[str, 15, 'cstring']
            datetime: Tag[int, LittleEndian, 'u32']
            lat: Tag[float, LittleEndian, "f32"]
            lon: Tag[float, LittleEndian, "f32"]
            code_msg: Tag[int, 'u8']

        if len(byte_string) > 29:
            blank = BlankExtended()
            res = blank.unpack_b(byte_string)
            return {
                'num_pack': res.num_pack,
                'type_message': res.type_message,
                'imei': str(res.imei, encoding='utf-8'),
                'datetime': res.datetime,
                'lat': res.lat,
                'lon': res.lon,
                'code_msg': res.code_msg
            }
        else:
            blank = Blank()
            res = blank.unpack_b(byte_string)
            return {
                'num_pack': res.num_pack,
                'type_message': res.type_message,
                'imei': str(res.imei, encoding='utf-8'),
                'datetime': res.datetime,
                'lat': res.lat,
                'lon': res.lon,
            }


input_data = [b'\x00\x01869586748696585\xfa\x12\xedfc.VB\xaa`EB',
              b'\x01\x01869586748696585\t\x15\xedf\x1b/VBB`EB',
              b'\x02\x02869586748696585+\x15\xedf\x9e/VB\xbe_EB\x03']

for string in input_data:
    res = TestProtocol.parse(string)
    print(res)
