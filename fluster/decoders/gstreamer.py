# Fluster - testing framework for decoders conformance
# Copyright (C) 2020, Fluendo, S.A.
#  Author: Pablo Marcos Oltra <pmarcos@fluendo.com>, Fluendo, S.A.
#  Author: Andoni Morales Alastruey <amorales@fluendo.com>, Fluendo, S.A.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

import shlex
from functools import lru_cache

from fluster.codec import Codec, PixelFormat
from fluster.decoder import Decoder, register_decoder
from fluster.utils import file_checksum, run_command, normalize_binary_cmd

PIPELINE_TPL = '{} filesrc location={} ! {} ! {} ! filesink location={}'


class GStreamer(Decoder):
    '''Base class for GStreamer decoders'''
    decoder_bin = None
    cmd = None
    caps = None
    gst_api = None
    api = None
    provider = None

    def __init__(self):
        super().__init__()
        self.name = f'{self.provider}-{self.codec.value}-{self.api}-Gst{self.gst_api}'
        self.description = f'{self.provider} {self.codec.value} {self.api} decoder for GStreamer {self.gst_api}'
        self.cmd = normalize_binary_cmd(self.cmd)

    def gen_pipeline(self, input_filepath: str, output_filepath: str, output_format: PixelFormat):
        '''Generate the GStreamer pipeline used to decode the test vector'''
        # pylint: disable=unused-argument
        return PIPELINE_TPL.format(self.cmd, input_filepath, self.decoder_bin, self.caps, output_filepath)

    def decode(self, input_filepath: str, output_filepath: str, output_format: PixelFormat, timeout: int,
               verbose: bool):
        '''Decode the test vector and do the checksum'''
        pipeline = self.gen_pipeline(
            input_filepath, output_filepath, output_format)
        run_command(shlex.split(pipeline), timeout=timeout, verbose=verbose)
        return file_checksum(output_filepath)

    @lru_cache(maxsize=None)
    def check(self, verbose):
        '''Check if GStreamer decoder is valid (better than gst-inspect)'''
        # pylint: disable=broad-except
        try:
            binary = normalize_binary_cmd(f'gst-launch-{self.gst_api}')
            pipeline = f'{binary} appsrc num-buffers=0 ! {self.decoder_bin} ! fakesink'
            run_command(shlex.split(pipeline), verbose=verbose)
        except Exception:
            return False
        return True


class GStreamer10(GStreamer):
    '''Base class for GStreamer 1.x decoders'''
    cmd = 'gst-launch-1.0'
    caps = 'video/x-raw'
    gst_api = '1.0'
    provider = 'GStreamer'

    def gen_pipeline(self, input_filepath: str, output_filepath: str, output_format: PixelFormat):
        caps = f'{self.caps} ! videoconvert dither=none ! video/x-raw,format={output_format.to_gst()}'
        return PIPELINE_TPL.format(self.cmd, input_filepath, self.decoder_bin, caps, output_filepath)


class GStreamer010(GStreamer):
    '''Base class for GStreamer 0.10 decoders'''
    cmd = 'gst-launch-0.10'
    caps = 'video/x-raw-yuv'
    gst_api = '0.10'
    provider = 'GStreamer'


@register_decoder
class GStreamerLibavH264(GStreamer10):
    '''GStreamer H.264 Libav decoder implementation for GStreamer 1.0'''
    codec = Codec.H264
    decoder_bin = ' h264parse ! avdec_h264 '
    api = 'Libav'
    hw_acceleration = False


@register_decoder
class GStreamerLibavH265(GStreamer10):
    '''GStreamer H.265 Libav decoder implementation for GStreamer 1.0'''
    codec = Codec.H265
    decoder_bin = ' h265parse ! avdec_h265 '
    api = 'Libav'
    hw_acceleration = False


@register_decoder
class GStreamerVaapiH265Gst10Decoder(GStreamer10):
    '''GStreamer H.265 VAAPI decoder implementation for GStreamer 1.0'''
    codec = Codec.H265
    decoder_bin = ' h265parse ! vaapih265dec '
    api = 'VAAPI'
    hw_acceleration = True


@register_decoder
class GStreamerMsdkH265Gst10Decoder(GStreamer10):
    '''GStreamer H.265 Intel MSDK decoder implementation for GStreamer 1.0'''
    codec = Codec.H265
    decoder_bin = ' h265parse ! msdkh265dec '
    api = 'MSDK'
    hw_acceleration = True


@register_decoder
class GStreamerNvdecH265Gst10Decoder(GStreamer10):
    '''GStreamer H.265 NVDEC decoder implementation for GStreamer 1.0'''
    codec = Codec.H265
    decoder_bin = ' h265parse ! nvh265dec '
    api = 'NVDEC'
    hw_acceleration = True


@register_decoder
class GStreamerD3d11H265Gst10Decoder(GStreamer10):
    '''GStreamer H.265 D3D11 decoder implementation for GStreamer 1.0'''
    codec = Codec.H265
    decoder_bin = ' h265parse ! d3d11h265dec '
    api = 'D3D11'
    hw_acceleration = True


@register_decoder
class GStreamerVaapiH264Gst10Decoder(GStreamer10):
    '''GStreamer H.264 VAAPI decoder implementation for GStreamer 1.0'''
    codec = Codec.H264
    decoder_bin = ' h264parse ! vaapih264dec '
    api = 'VAAPI'
    hw_acceleration = True


@register_decoder
class GStreamerMsdkH264Gst10Decoder(GStreamer10):
    '''GStreamer H.264 Intel MSDK decoder implementation for GStreamer 1.0'''
    codec = Codec.H264
    decoder_bin = ' h264parse ! msdkh264dec '
    api = 'MSDK'
    hw_acceleration = True


@register_decoder
class GStreamerNvdecH264Gst10Decoder(GStreamer10):
    '''GStreamer H.264 NVDEC decoder implementation for GStreamer 1.0'''
    codec = Codec.H264
    decoder_bin = ' h264parse ! nvh264dec '
    api = 'NVDEC'
    hw_acceleration = True


@register_decoder
class GStreamerD3d11H264Gst10Decoder(GStreamer10):
    '''GStreamer H.264 D3D11 decoder implementation for GStreamer 1.0'''
    codec = Codec.H264
    decoder_bin = ' h264parse ! d3d11h264dec '
    api = 'D3D11'
    hw_acceleration = True


@register_decoder
class FluendoH265Gst10Decoder(GStreamer10):
    '''Fluendo H.265 software decoder implementation for GStreamer 1.0'''
    codec = Codec.H265
    decoder_bin = ' h265parse ! fluh265dec '
    provider = 'Fluendo'
    api = 'SW'


@register_decoder
class FluendoH265Gst010Decoder(GStreamer010):
    '''Fluendo H.265 software decoder implementation for GStreamer 0.10'''
    codec = Codec.H265
    decoder_bin = ' h265parse ! fluh265dec '
    provider = 'Fluendo'
    api = 'SW'


@register_decoder
class FluendoH264Gst10Decoder(GStreamer10):
    '''Fluendo H.264 software decoder implementation for GStreamer 1.0'''
    codec = Codec.H264
    decoder_bin = ' h264parse ! fluh264dec '
    provider = 'Fluendo'
    api = 'SW'


@register_decoder
class FluendoH264Gst010Decoder(GStreamer010):
    '''Fluendo H.264 software decoder implementation for GStreamer 0.10'''
    codec = Codec.H264
    decoder_bin = ' fluh264dec '
    provider = 'Fluendo'
    api = 'SW'


@register_decoder
class FluendoH264VAGst10Decoder(GStreamer10):
    '''Fluendo H.264 hardware decoder implementation for GStreamer 1.0'''
    codec = Codec.H264
    decoder_bin = ' h264parse ! fluvadec '
    provider = 'Fluendo'
    api = 'HW'
    hw_acceleration = True


@register_decoder
class FluendoH265VAGst10Decoder(GStreamer10):
    '''Fluendo H.265 hardware decoder implementation for GStreamer 1.0'''
    codec = Codec.H265
    decoder_bin = ' h265parse ! fluvadec '
    provider = 'Fluendo'
    api = 'HW'
    hw_acceleration = True
