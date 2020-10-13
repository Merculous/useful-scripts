# Compress

Uses archivers: bsc, bzip2, gzip, nanozip, precomp, pcompress, p7zip, xz, zpaq to achieve max compression

# 30to60

Uses ffmpeg to convert any supported video to a h264, 1280x720 (16:9 aspect ratio), 60fps, 6Mbps, mp4 file. It uses motion interpolation (basically blends frames) to achieve
60fps or as most call it, smooth motion.

# ldd-copy

Copies libraries used in a binary printed by ldd. Finds real path, which means it doesn't copy the symlink, and follows the symlink instead.
