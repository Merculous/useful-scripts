# Compress

Uses xz, 7zip, and zpaq to achieve maximum compression

# 30to60

Uses ffmpeg to convert any supported video to a h264, 1280x720, 60fps, 6Mbps, mp4 file. It uses motion interpolation (basically blends frames) to achieve
60fps or as most call it, smooth motion.

# ldd-copy

Copies libraries used in a binary printed by ldd. Finds real path, which means it doesn't copy the symlink, and follows the symlink instead.
