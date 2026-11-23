<!-- Source: https://docs.yoctoproject.org/scarthgap/profile-manual/arch.html (converted from singleindex.html). License: see LICENSE-docs.md in this folder. -->

#### 2 Overall Architecture of the Linux Tracing and Profiling Tools

##### 2.1 Architecture of the Tracing and Profiling Tools

It may seem surprising to see a section covering an ‘overall architecture’ for what seems to be a random collection of tracing tools that together make up the Linux tracing and profiling space. The fact is, however, that in recent years this seemingly disparate set of tools has started to converge on a ‘core’ set of underlying mechanisms:

- static tracepoints

- dynamic tracepoints

  - kprobes

  - uprobes

- the perf_events subsystem

- debugfs

Tying it Together

Rather than enumerating here how each tool makes use of these common mechanisms, textboxes like this will make note of the specific usages in each tool as they come up in the course of the text.
