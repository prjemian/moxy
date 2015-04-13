====================================================
MOXY: EPICS GUI support for a set of motor positions
====================================================

*moxy*: EPICS GUI support for a set of motor positions

:see: https://github.com/prjemian/moxy/

.. sidebar:: 2014-05-29, PRJ

   This project is being rewritten at this time.
   The entire infrastructure is being redesigned so do not expect
   anything here to remain constant.

*moxy* (an EPICS GUI tool) provides support for a set of positioners
(EPICS motor records or similar) by allowing users to define a table 
of known positions and providing a one-button click to drive the set 
of positioners to a specific setting in the table.  Also can record 
current position into a setting.

Several sets of positioners can be configured.  (Each set is 
separate.)  In fact, the positioners do not have to be motors,
but can be any type of EPICS PV that will accept a numeric value.

*moxy* requires these Python packages:

===============   ===============   ====================================================================
package           version           website
===============   ===============   ====================================================================
*PyQt4*           >= 4              http://http://www.riverbankcomputing.com/software/pyqt/intro ([#]_)
*PyEpics*         >= 3.2            http://cars9.uchicago.edu/software/python/pyepics3/
*bcdaqwidgets*    >= 2015.0413.0    http://subversion.xray.aps.anl.gov/admin_bcdaext/BcdaQWidgets
===============   ===============   ====================================================================

.. [#] this project developed with PyQt4 >= 4.11.3

And, this tool is useless without:
* *EPICS* (http://www.aps.anl.gov/epics)
* EPICS *motor* record (http://www.aps.anl.gov/bcda/synApps/motor)
* EPICS IOC server running one or more *motor* instances
  (or a set of PVs that emulate the *motor* interface).

In the Graphical User Interface (GUI), tooltips are provided for 
most items.  Moving and pausing the mouse over a widget (GUI 
component such as a button or a label) will cause a terse description 
of that widget to be displayed. Moving the mouse away will cause that 
tooltip to disappear. 

For more help, explanations are provided in the documentation.
