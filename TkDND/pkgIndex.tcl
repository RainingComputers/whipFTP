#
# Tcl package index file
#

switch [tk windowingsystem] {
  x11 {
    switch [lindex $::tcl_platform(os) 0] {
      Linux {
        switch [lindex $::tcl_platform(machine) 0] {
          x86_64 {
            package ifneeded tkdnd 2.8 \
              "source \{$dir/tkdnd.tcl\} ; \
               tkdnd::initialise \{$dir\} libtkdnd2.8.so tkdnd"
          }
          i686 {
            package ifneeded tkdnd 2.8 \
              "source \{$dir/tkdnd.tcl\} ; \
               tkdnd::initialise \{$dir\} lib32tkdnd2.8.so tkdnd"              
          }
          default {
            error "unknown architecture"
          }
        }
      }
      FreeBSD {
        switch [lindex $::tcl_platform(machine) 0] {
          amd64 {
            package ifneeded tkdnd 2.8 \
              "source \{$dir/tkdnd.tcl\} ; \
               tkdnd::initialise \{$dir\} libtkdnd2.8_FreeBSD.so tkdnd"
          }
          i386 {
            package ifneeded tkdnd 2.8 \
              "source \{$dir/tkdnd.tcl\} ; \
               tkdnd::initialise \{$dir\} lib32tkdnd2.8_FreeBSD.so tkdnd"
          }
          default {
            error "unknown architecture"
          }
        }        
      }
      default {
        error "unknown x11 platform"
      }
    }
  }
  win32 -
  windows {
    switch [lindex $::tcl_platform(machine) 0] {
      intel {
        package ifneeded tkdnd 2.8 \
          "source \{$dir/tkdnd.tcl\} ; \
           tkdnd::initialise \{$dir\} lib32tkdnd2.8[info sharedlibextension] tkdnd"
      }
      amd64 {
        package ifneeded tkdnd 2.8 \
          "source \{$dir/tkdnd.tcl\} ; \
           tkdnd::initialise \{$dir\} libtkdnd2.8[info sharedlibextension] tkdnd"
      }
    }
  }
  aqua  {
    package ifneeded tkdnd 2.8 \
      "source \{$dir/tkdnd.tcl\} ; \
       tkdnd::initialise \{$dir\} libtkdnd2.8[info sharedlibextension] tkdnd"
  }
  default {
    error "unknown Tk windowing system"
  }
}
