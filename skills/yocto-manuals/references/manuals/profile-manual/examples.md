<!-- Source: https://docs.yoctoproject.org/scarthgap/profile-manual/examples.html (converted from singleindex.html). License: see LICENSE-docs.md in this folder. -->

#### 4 Real-World Examples

This chapter contains real-world examples.

##### 4.1 Slow Write Speed on Live Images

In one of our previous releases (denzil), users noticed that booting off of a live image and writing to disk was noticeably slower. This included the boot itself, especially the first one, since first boots tend to do a significant amount of writing due to certain post-install scripts.

The problem (and solution) was discovered by using the Yocto tracing tools, in this case ‘perf stat’, ‘perf script’, ‘perf record’ and ‘perf report’.

See all the unvarnished details of how this bug was diagnosed and solved here: Yocto Bug #3049

The Yocto Project ®

<docs@lists.yoctoproject.org>

Permission is granted to copy, distribute and/or modify this document under the terms of the Creative Commons Attribution-Share Alike 2.0 UK: England & Wales as published by Creative Commons.

To report any inaccuracies or problems with this (or any other Yocto Project) manual, or to send additions or changes, please send email/patches to the Yocto Project documentation mailing list at `docs@lists.yoctoproject.org` or log into the Libera Chat `#yocto` channel.
