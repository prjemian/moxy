#! /usr/bin/env python


'''
Moxy: handle XML configuration file
'''


import os
from lxml import etree
import moxygroup


XML_CONFIG_FILE = os.path.join(os.path.abspath(os.path.split(__file__)[0]), 'config.xml')
XML_ROOT_TAG = 'moxy'
XML_MOXY_VERSION = '3.0'


class NotMoxyXmlDocument(Exception): pass


def isAttributeTrue(node, attribute):
    '''Is the XML boolean attribute value True or False (not true, that is)?'''
    return node.get(attribute, '').lower() == 'true'


def read_config(config_file):
    '''get configuration from named XML file
    
    :param str config_file: XML file (with optional path)
    :returns []: preferences dictionary, group list, and selected group number
    '''
    doc = etree.parse(config_file)
    root = doc.getroot()

    if root.tag != XML_ROOT_TAG:
        msg = 'invalid root tag: ' + root.tag
        msg += '\n  should be: ' + XML_ROOT_TAG
        raise NotMoxyXmlDocument, msg
    if root.get('version', '')  != XML_MOXY_VERSION:
        msg = 'invalid version attribute: ' + root.get('version', '')
        msg += '\n  should be: ' + XML_MOXY_VERSION
        raise NotMoxyXmlDocument, msg

    preferences = read_preferences(config_file, root)
    grouplist, selected_group = read_groups(config_file, root)
    return preferences, grouplist, selected_group


def read_preferences(config_file, root):
    preferences = dict()
    prefs_node = root.find('preferences')
    if prefs_node is not None:
        for item in ('group.SKIP_DELETE_CONFIRMATIONS',
                     'table.SKIP_DELETE_CONFIRMATIONS',
                     'row.SKIP_DELETE_CONFIRMATIONS',):
            label, setting = item.split('.')
            node = prefs_node.find(item)
            if node is not None:
                preferences[label] = {setting: isAttributeTrue(node,'value')}
    return preferences


def read_groups(config_file, root):
    grouplist = []
    selected_group = None
    for group_number, group_node in enumerate(root.findall('group')):
        group = moxygroup.MoxyGroup(group_node.get('name', ''))
        grouplist.append( group )

        if selected_group is None and isAttributeTrue(group_node,'selected'):
            selected_group = group_number

        # parse and store axes of this group
        group.axislist = read_axes(group_node, config_file, group)
        axis_names = [axis.name for axis in group.axislist]

        # parse and store tables of this group
        group.tablelist = read_tables(group_node, config_file, axis_names, group)
    return grouplist, selected_group


def read_axes(parent_node, config_file, group):
    axislist = []
    for axis_node in parent_node.findall('axis'):
        axislist.append( moxygroup.GroupAxis(axis_node.get('name', '') ) )
    return axislist


def read_tables(parent_node, config_file, axis_names, group):
    tablelist = []
    selected_table = None
    for table_number, table_node in enumerate(parent_node.findall('table')):
        table = moxygroup.GroupTable(table_node.get('name', ''))
        tablelist.append( table )

        if selected_table is None and isAttributeTrue(table_node, 'selected'):
            selected_table = table_number
        
        selected_row = None
        for row_number, row_node in enumerate(table_node.findall('row')):
            row = moxygroup.TableRow(row_node.get('name', ''))
            table.rowlist.append( row )

            if selected_row is None and isAttributeTrue(row_node, 'selected'):
                selected_row = row_number
            
            row.positionlist = read_positions(row_node, config_file, axis_names, group, table, row)
        table.selected_row = selected_row
    group.selected_table = selected_table
    return tablelist


def read_positions(parent_node, config_file, axis_names, group, table, row):
    position_list = []
    for pos_node in parent_node.findall('position'):
        pos_name = pos_node.get('name', '')
        try:
            if pos_name not in axis_names:
                msg = 'Configuration file inconsistency: Position name not a defined axis: '
                msg += '\n  file: ' + config_file
                msg += '\n  group: ' + group.name
                msg += '\n  table: ' + table.name
                msg += '\n  row: ' + row.name
                msg += '\n  position: ' + pos_name
                msg += '\n  defined axes: ' + str(axis_names)
                raise moxygroup.PositionInconsistency, msg
            pos_value = pos_node.get('value', '')
            axis = group.axislist[group.axisNameToIndex(pos_name)]
            pos = moxygroup.RowPosition(pos_name, pos_value, group_axis_obj=axis)
            row.positionlist.append( pos )
        except moxygroup.PositionInconsistency, exc:
            print exc   # TODO: report/handle differently
            break       # skip this row due to inconsistency
    return position_list


def main():
    # read config.xml and create MoxyGroup(s)
    prefs, moxygroups, selected_group = read_config(XML_CONFIG_FILE)
    print prefs
    print moxygroups
    print selected_group


if __name__ == '__main__':
    main()
