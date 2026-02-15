#
# █▀▄ █▀█ ▄▀█ █░▄░█ ░░ ▀█▀ ▄▀█ █▄▄
# █▄▀ █▀▄ █▀█ ▀▄▀▄▀ ▄▄ ░█░ █▀█ █▄█
#
# Custom tab decorations with rounded boxes and icons

import re


from kitty.fast_data_types import Screen
from kitty.tab_bar import (DrawData, ExtraData, TabBarData, as_rgb, draw_title)

icon_map = {
        ' ': ['vim'],
        ' ': ['nvim', 'Nvim'],
        ' ': ['tmux', 'zellij'],
        ' ': ['python', 'python3', 'ipython', 'ipython3'],
        '󰒲 ': ['lazygit'],
        '󱎴 ': ['htop', 'btop', 'nvidia-smi', 'nvtop'],
        '󰇥 ': ['yazi'],
        ' ': ['fzf'],
    }


substitutions = {
        'Documents': '󰈙',
        'Downloads': '',
        'Music': '󰝚',
        'Pictures': '',
        'Developer': '󰲋',
        #'~': ''
    }


def get_title_icon (title: str) -> str:
    for icon, keywords in icon_map.items():
        for keyword in keywords:
            if keyword in title.split():
                return icon

    return None


def rewrite_title (title: str) -> str:
    for k, v in substitutions.items ():
        title = title.replace (k, v)
    return title


def draw_tab (
        draw_data: DrawData,
        screen: Screen,
        tab: TabBarData,
        before: int,
        max_tab_length: int,
        index: int,
        is_last: bool,
        extra_data: ExtraData,
    ) -> int:

    tab_fg = screen.cursor.fg
    tab_bg = screen.cursor.bg
    left_sep, right_sep = ('█', '█')

    def draw_sep (which: str) -> None:
        screen.cursor.bg = tab_fg
        screen.cursor.fg = tab_bg
        screen.draw(which)
        screen.cursor.bg = tab_bg
        screen.cursor.fg = tab_fg

    icon = get_title_icon (tab.title)
    icon_width = 0
    if icon:
        icon_width = 2

    start_draw = 2

    # If this is the first tab to be drawn, add a space.
    if screen.cursor.x == 0:
        screen.cursor.bg = tab_fg
        screen.draw(' ')
        start_draw = 1
        screen.cursor.bg = tab_bg
        screen.cursor.fg = tab_fg

    if max_tab_length <= (5 + icon_width):
        draw_sep (left_sep)
        screen.draw ('…')
        draw_sep (right_sep)
    else:
        draw_sep (left_sep)
        if icon:
            screen.draw (icon)
        screen.draw (rewrite_title (tab.title))
        extra = screen.cursor.x + start_draw - before - max_tab_length
        if extra > 0 and extra + 1 < screen.cursor.x:
            screen.cursor.x -= extra + 1
            screen.draw('…')
        draw_sep (right_sep)

    if not is_last:
        draw_sep (' ')

    return screen.cursor.x

