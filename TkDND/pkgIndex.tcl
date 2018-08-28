#
# Tcl package index file
#

switch [tk windowingsystem] {
  x11 {
    switch [lindex $::tcl_platform(os) 0] {
      Linux {
        package ifneeded tkdnd 2.8 \
          "source \{$dir/tkdnd.tcl\} ; \
           tkdnd::initialise \{$dir\} libtkdnd2.8.so tkdnd"
      }
      FreeBSD {
        package ifneeded tkdnd 2.8 \
          "source \{$dir/tkdnd.tcl\} ; \
           tkdnd::initialise \{$dir\} libtkdnd2.8_FreeBSD.so tkdnd"        
      }
      default {
        error "unknown x11 platform"
      }
    }
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