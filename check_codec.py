import struct

f = open(r'C:\Users\Arturo\Desktop\Django_Porcino\static\img\cerdos.mp4', 'rb')
data = f.read()
f.close()

def find_box(data, target, start, end):
    pos = start
    while pos < end - 8:
        size = struct.unpack('>I', data[pos:pos+4])[0]
        box = data[pos+4:pos+8].decode('ascii', errors='replace')
        if size <= 0 or pos + size > end:
            return None
        if box == target:
            return (pos, size)
        pos += size
    return None

moov = find_box(data, 'moov', 0, len(data))
if moov:
    moov_start, moov_size = moov
    trak = find_box(data, 'trak', moov_start+8, moov_start+moov_size)
    if trak:
        trak_start, trak_size = trak
        mdia = find_box(data, 'mdia', trak_start+8, trak_start+trak_size)
        if mdia:
            mdia_start, mdia_size = mdia
            minf = find_box(data, 'minf', mdia_start+8, mdia_start+mdia_size)
            if minf:
                minf_start, minf_size = minf
                stbl = find_box(data, 'stbl', minf_start+8, minf_start+minf_size)
                if stbl:
                    stbl_start, stbl_size = stbl
                    stsd = find_box(data, 'stsd', stbl_start+8, stbl_start+stbl_size)
                    if stsd:
                        stsd_start, stsd_size = stsd
                        entry_pos = stsd_start + 16
                        entry_size = struct.unpack('>I', data[entry_pos:entry_pos+4])[0]
                        codec = data[entry_pos+4:entry_pos+8].decode('ascii', errors='replace')
                        print(f'Codec: {codec} (size={entry_size})')
                        
                        codec_data = data[entry_pos:entry_pos+min(entry_size, 80)]
                        print('Hex:', codec_data.hex())
