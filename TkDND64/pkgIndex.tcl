#
# Tcl package index file
#

switch [tk windowingsystem] {
  x11 {
    package ifneeded tkdnd 2.8 \
      "source \{$dir/tkdnd.tcl\} ; \
       tkdnd::initialise \{$dir\} libtkdnd2.8.so tkdnd"
  }
  win32 -
  windows {
    package ifneeded tkdnd 2.8 \
      "source \{$dir/tkdnd.tcl\} ; \
       tkdnd::initialise \{$dir\} libtkdnd2.8[info sharedlibextension] tkdnd"
  }
  default {
    error "unknown Tk windowing system"
  }
}
