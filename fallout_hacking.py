#!/usr/bin/env python3
"""
Fallout 4 Hacking Mini-Game Recreation
A command-line playable version using curses - Pixel perfect recreation
"""

import curses
import random
import argparse
import sys
from typing import List, Tuple, Optional, Set

# Word lists for different lengths
WORD_LISTS = {
    4: ['TEST', 'DATA', 'CODE', 'NODE', 'FILE', 'DISK', 'BOOT', 'CORE', 'LINK', 'LOAD',
         'KEYS', 'LOCK', 'USER', 'PASS', 'ROOT', 'HOST', 'PORT', 'PATH', 'NAME', 'TYPE'],
    5: ['START', 'RESET', 'LOGIN', 'LOGOUT', 'ADMIN', 'SUPER', 'POWER', 'SYSTEM', 'MEMORY',
         'DRIVE', 'FOLDER', 'FILES', 'PRINT', 'INPUT', 'OUTPUT', 'SCREEN', 'MOUSE', 'KEYBOARD',
         'SPEAKER', 'PHONE', 'TABLE', 'CHAIR', 'DESK', 'WINDOW', 'DOOR', 'LIGHT', 'POWER',
         'WATER', 'FIRE', 'EARTH', 'WIND', 'SPACE', 'TIME', 'CLOCK', 'WATCH', 'TIMER'],
    6: ['SERVER', 'CLIENT', 'ROUTER', 'SWITCH', 'MODEM', 'PROXY', 'FIREWALL', 'NETWORK',
         'WIRELESS', 'BLUETOOTH', 'ETHERNET', 'BROWSER', 'CHROME', 'FIREFOX', 'SAFARI',
         'OPERA', 'EDGE', 'PYTHON', 'JAVA', 'RUBY', 'GOLANG', 'RUST', 'SWIFT', 'KOTLIN',
         'SCRIPT', 'SHELL', 'BASH', 'ZSH', 'FISH', 'TERMINAL', 'CONSOLE', 'COMMAND'],
    7: ['PROGRAM', 'SOFTWARE', 'HARDWARE', 'COMPUTER', 'MONITOR', 'KEYBOARD', 'PRINTER',
         'SCANNER', 'SPEAKER', 'HEADSET', 'WEBCAM', 'CAMERA', 'MICROPHONE', 'PROJECTOR',
         'DISPLAY', 'STORAGE', 'DATABASE', 'BACKEND', 'FRONTEND', 'FULLSTACK', 'DEVELOPER',
         'ENGINEER', 'MANAGER', 'DIRECTOR', 'EXECUTIVE', 'PRESIDENT', 'OFFICER', 'SOLDIER'],
    8: ['TERMINAL', 'KEYBOARD', 'MONITOR', 'PROCESSOR', 'MAINFRAME', 'SUPERCOMPUTER',
         'WORKSTATION', 'NOTEBOOK', 'LAPTOP', 'TABLET', 'SMARTPHONE', 'CELLPHONE', 'TELEPHONE',
         'FACSIMILE', 'TELETYPE', 'TYPEWRITER', 'CALCULATOR', 'SPREADSHEET', 'WORDPROCESSOR',
         'DATABASE', 'SPREADSHEET', 'PRESENTATION', 'GRAPHICAL', 'INTERFACE', 'PROTOCOL'],
    9: ['MAINFRAME', 'WORKSTATION', 'SUPERCOMPUTER', 'MICROPROCESSOR', 'TRANSMITTER',
         'RECEIVER', 'ANTENNA', 'SATELLITE', 'BROADCAST', 'TELEVISION', 'RADIO', 'TELEGRAPH',
         'TELEPHONE', 'CELLPHONE', 'SMARTPHONE', 'TABLET', 'NOTEBOOK', 'LAPTOP', 'COMPUTER',
         'PERIPHERAL', 'ACCESSORY', 'COMPONENT', 'ELECTRONIC', 'DIGITAL', 'ANALOG'],
    10: ['MAINFRAMES', 'WORKSTATIONS', 'SUPERCOMPUTERS', 'MICROPROCESSORS', 'TRANSMITTERS',
          'RECEIVERS', 'ANTENNAS', 'SATELLITES', 'BROADCASTS', 'TELEVISIONS', 'RADIOS',
          'TELEGRAPHS', 'TELEPHONES', 'CELLPHONES', 'SMARTPHONES', 'TABLETS', 'NOTEBOOKS',
          'LAPTOPS', 'COMPUTERS', 'PERIPHERALS', 'ACCESSORIES', 'COMPONENTS', 'ELECTRONICS'],
    11: ['MICROPROCESSOR', 'MAINFRAME', 'WORKSTATION', 'SUPERCOMPUTER', 'TRANSMITTER',
          'RECEIVER', 'ANTENNA', 'SATELLITE', 'BROADCAST', 'TELEVISION', 'RADIO', 'TELEGRAPH',
          'TELEPHONE', 'CELLPHONE', 'SMARTPHONE', 'TABLET', 'NOTEBOOK', 'LAPTOP', 'COMPUTER',
          'PERIPHERAL', 'ACCESSORY', 'COMPONENT', 'ELECTRONIC', 'DIGITAL', 'ANALOG'],
    12: ['MICROPROCESSORS', 'MAINFRAMES', 'WORKSTATIONS', 'SUPERCOMPUTERS', 'TRANSMITTERS',
          'RECEIVERS', 'ANTENNAS', 'SATELLITES', 'BROADCASTS', 'TELEVISIONS', 'RADIOS',
          'TELEGRAPHS', 'TELEPHONES', 'CELLPHONES', 'SMARTPHONES', 'TABLETS', 'NOTEBOOKS',
          'LAPTOPS', 'COMPUTERS', 'PERIPHERALS', 'ACCESSORIES', 'COMPONENTS', 'ELECTRONICS'],
    13: ['MICROPROCESSORS', 'MAINFRAMES', 'WORKSTATIONS', 'SUPERCOMPUTERS', 'TRANSMITTERS',
          'RECEIVERS', 'ANTENNAS', 'SATELLITES', 'BROADCASTS', 'TELEVISIONS', 'RADIOS',
          'TELEGRAPHS', 'TELEPHONES', 'CELLPHONES', 'SMARTPHONES', 'TABLETS', 'NOTEBOOKS',
          'LAPTOPS', 'COMPUTERS', 'PERIPHERALS', 'ACCESSORIES', 'COMPONENTS', 'ELECTRONICS'],
    14: ['MICROPROCESSORS', 'MAINFRAMES', 'WORKSTATIONS', 'SUPERCOMPUTERS', 'TRANSMITTERS',
          'RECEIVERS', 'ANTENNAS', 'SATELLITES', 'BROADCASTS', 'TELEVISIONS', 'RADIOS',
          'TELEGRAPHS', 'TELEPHONES', 'CELLPHONES', 'SMARTPHONES', 'TABLETS', 'NOTEBOOKS',
          'LAPTOPS', 'COMPUTERS', 'PERIPHERALS', 'ACCESSORIES', 'COMPONENTS', 'ELECTRONICS'],
    15: ['MICROPROCESSORS', 'MAINFRAMES', 'WORKSTATIONS', 'SUPERCOMPUTERS', 'TRANSMITTERS',
          'RECEIVERS', 'ANTENNAS', 'SATELLITES', 'BROADCASTS', 'TELEVISIONS', 'RADIOS',
          'TELEGRAPHS', 'TELEPHONES', 'CELLPHONES', 'SMARTPHONES', 'TABLETS', 'NOTEBOOKS',
          'LAPTOPS', 'COMPUTERS', 'PERIPHERALS', 'ACCESSORIES', 'COMPONENTS', 'ELECTRONICS']
}

# Special characters for bracket sequences
BRACKET_CHARS = '!@#$%^&*()_+-=[]{}|;:,.<>?/~`'
HEX_CHARS = '0123456789ABCDEF'

DIFFICULTY_CONFIG = {
    1: {'name': 'VERY EASY', 'min_len': 4, 'max_len': 5, 'word_count': 8, 'attempts': 5, 'retry': True},
    2: {'name': 'EASY', 'min_len': 6, 'max_len': 8, 'word_count': 10, 'attempts': 5, 'retry': False},
    3: {'name': 'AVERAGE', 'min_len': 9, 'max_len': 10, 'word_count': 12, 'attempts': 5, 'retry': False},
    4: {'name': 'HARD', 'min_len': 11, 'max_len': 12, 'word_count': 14, 'attempts': 5, 'retry': False},
    5: {'name': 'VERY HARD', 'min_len': 13, 'max_len': 15, 'word_count': 16, 'attempts': 5, 'retry': False}
}


class GridLine:
    def __init__(self, address: str, content: str, word: Optional[str] = None, 
                 word_start: int = -1, bracket_info: Optional[Tuple[int, int, str]] = None,
                 is_dud: bool = False, removed: bool = False, bracket_used: bool = False):
        self.address = address  # Hex address like "0xFA8C"
        self.content = content  # Full content string
        self.word = word  # Word embedded in content (if any)
        self.word_start = word_start  # Starting position of word in content
        self.bracket_info = bracket_info  # (start, end, bracket_pair) if brackets exist
        self.is_dud = is_dud  # True if this is a dud word
        self.removed = removed  # True if this dud has been removed
        self.bracket_used = bracket_used  # True if bracket has been used


class HackingGame:
    def __init__(self, difficulty: int):
        self.difficulty = difficulty
        self.config = DIFFICULTY_CONFIG[difficulty]
        self.password_length = random.randint(self.config['min_len'], self.config['max_len'])
        self.attempts_left = self.config['attempts']
        self.max_attempts = self.config['attempts']
        self.words = self._generate_words()
        self.password = random.choice(self.words)
        self.grid_lines = self._generate_grid()
        self.cursor_row = 0
        self.cursor_col = 0
        self.game_over = False
        self.won = False
        self.locked_out = False
        self.last_guess = None
        self.last_match_count = 0
        self.dud_words = set()
        self.output_history = []
        self.replenish_bracket_used = False

    def _generate_words(self) -> List[str]:
        word_list = WORD_LISTS.get(self.password_length, WORD_LISTS[4])
        word_count = self.config['word_count']
        available_words = [w for w in word_list if len(w) == self.password_length]
        
        if len(available_words) < word_count:
            available_words = [w.upper() for w in available_words]
            while len(available_words) < word_count:
                available_words.append(''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') 
                                              for _ in range(self.password_length)))
        
        return random.sample(available_words, min(word_count, len(available_words)))

    def _generate_grid(self) -> List[GridLine]:
        lines = []
        num_columns = 2  # Two columns of content
        num_rows = 17  # Fixed 17 rows per column
        total_cells = num_rows * num_columns
        
        # Calculate number of bracket pairs needed
        num_duds = len(self.words) - 1  # All words except password are duds
        bracket_counts = {
            1: num_duds + 1,  # One bracket pair for each dud + one reset
            2: num_duds - 1 + 1,  # One bracket pair less than duds + one reset
            3: num_duds - 1 + 1,  # One bracket pair less than duds + one reset
            4: num_duds - 2 + 1,  # Two bracket pairs less than duds + one reset
            5: num_duds - 3 + 1   # Three bracket pairs less than duds + one reset
        }
        num_bracket_pairs = max(1, bracket_counts.get(self.difficulty, 2))
        
        # Generate hex addresses for all cells
        addresses = []
        for i in range(total_cells):
            addr = '0x' + ''.join(random.choice(HEX_CHARS) for _ in range(4))
            addresses.append(addr)
        
        # Create all grid lines with random characters first
        for i in range(total_cells):
            content = self._create_line_content(None)
            line = GridLine(
                addresses[i],
                content['content'],
                content['word'],
                content['word_start'],
                content['bracket_info']
            )
            lines.append(line)
        
        # Randomly select positions for words (spread across all rows)
        word_positions = random.sample(range(total_cells), len(self.words))
        
        # Decide which word positions will have bracket sequences
        bracket_line_indices = set()
        if num_bracket_pairs > 0:
            bracket_line_indices = set(random.sample(word_positions, min(num_bracket_pairs, len(word_positions))))
        
        # Place words at selected positions
        for word_idx, line_idx in enumerate(word_positions):
            has_bracket = line_idx in bracket_line_indices
            
            if has_bracket:
                # Create line with both word AND bracket sequence
                content = self._create_line_content_with_both(self.words[word_idx])
            else:
                # Create line with just word
                content = self._create_line_content(self.words[word_idx])
            
            lines[line_idx] = GridLine(
                addresses[line_idx],
                content['content'],
                content['word'],
                content['word_start'],
                content['bracket_info'],
                is_dud=(self.words[word_idx] != self.password)
            )
        
        # Ensure password is in the grid
        password_in_grid = any(line.word == self.password for line in lines)
        if not password_in_grid:
            # Replace a random dud word with password
            non_password_lines = [i for i, line in enumerate(lines) if line.word and line.word != self.password]
            if non_password_lines:
                replace_idx = random.choice(non_password_lines)
                old_line = lines[replace_idx]
                new_content = self._create_line_content(self.password)
                lines[replace_idx] = GridLine(
                    old_line.address,
                    new_content['content'],
                    self.password,
                    new_content['word_start'],
                    new_content['bracket_info'],
                    is_dud=False
                )
        
        return lines

    def _create_line_content(self, word: Optional[str] = None, force_bracket: bool = False) -> dict:
        content_length = 16
        bracket_pairs = ['()', '[]', '{}', '<>']
        safe_chars = ':;\'",.!=$*^\\|][)(}{><'  # Safe characters that won't interfere with highlighting
        non_bracket_chars = '!@#$%^&*_-+|;:,.?/~`'  # Characters that aren't brackets
        
        if word:
            # Always embed the word when provided
            word_start = random.randint(0, max(0, content_length - len(word)))
            content = []
            
            for i in range(content_length):
                if word_start <= i < word_start + len(word):
                    content.append(word[i - word_start])
                else:
                    # Ensure character before word is a safe character
                    if i == word_start - 1:
                        content.append(random.choice(safe_chars))
                    else:
                        content.append(random.choice(non_bracket_chars))
            
            return {
                'content': ''.join(content),
                'word': word,
                'word_start': word_start,
                'bracket_info': None
            }
        
        # No word provided - just random characters (no brackets)
        content = ''.join(random.choice(non_bracket_chars) for _ in range(content_length))
        return {
            'content': content,
            'word': None,
            'word_start': -1,
            'bracket_info': None
        }

    def _create_line_content_with_both(self, word: str) -> dict:
        """Create a line with both a word and a bracket sequence"""
        content_length = 16
        bracket_pairs = ['()', '[]', '{}', '<>']
        
        # Randomly position the word
        word_start = random.randint(0, max(0, content_length - len(word)))
        
        # Randomly position the bracket sequence (not overlapping with word)
        bracket_pair = random.choice(bracket_pairs)
        open_bracket = bracket_pair[0]
        close_bracket = bracket_pair[1]
        
        # Find a valid position for brackets that doesn't overlap with word
        max_attempts = 10
        for _ in range(max_attempts):
            bracket_start = random.randint(0, content_length - 6)
            bracket_end = bracket_start + random.randint(1, 4)  # Ensure bracket_end > bracket_start
            
            # Check if brackets overlap with word
            word_end = word_start + len(word)
            brackets_overlap = (bracket_start < word_end and bracket_end >= word_start)
            
            if not brackets_overlap:
                break
        else:
            # If we couldn't find a non-overlapping position, just place brackets
            bracket_start = random.randint(0, content_length - 6)
            bracket_end = bracket_start + random.randint(1, 4)  # Ensure bracket_end > bracket_start
        
        # Generate content with both word and brackets
        content = []
        safe_chars = ':;\'",.!=$*^\\|][)(}{><'  # Safe characters that won't interfere with highlighting
        non_bracket_chars = '!@#$%^&*_-+|;:,.?/~`'  # Characters that aren't brackets
        
        for i in range(content_length):
            # Prioritize word characters first
            if word_start <= i < word_start + len(word):
                content.append(word[i - word_start])
            elif i == bracket_start:
                content.append(open_bracket)
            elif i == bracket_end:
                content.append(close_bracket)
            else:
                # Ensure character before word is a safe character
                if i == word_start - 1:
                    content.append(random.choice(safe_chars))
                else:
                    content.append(random.choice(non_bracket_chars))
        
        return {
            'content': ''.join(content),
            'word': word,
            'word_start': word_start,
            'bracket_info': (bracket_start, bracket_end, bracket_pair)
        }

    def get_current_highlight(self) -> Tuple[int, int]:
        """Get the start and end positions of the current highlight"""
        line = self.grid_lines[self.cursor_row]

        # Don't highlight if word or bracket has been removed/used
        if line.removed:
            return (self.cursor_col, self.cursor_col + 1)

        # Check if cursor is on a word
        if line.word and line.word_start <= self.cursor_col < line.word_start + len(line.word):
            return (line.word_start, line.word_start + len(line.word))

        # Check if cursor is on a bracket
        if line.bracket_info and not line.bracket_used:
            bracket_start, bracket_end, _ = line.bracket_info
            if self.cursor_col == bracket_start:
                return (bracket_start, bracket_end + 1)

        return (self.cursor_col, self.cursor_col + 1)

    def get_current_word(self) -> Optional[str]:
        """Get the word at current cursor position"""
        line = self.grid_lines[self.cursor_row]
        
        if line.word and not line.removed and line.word_start <= self.cursor_col < line.word_start + len(line.word):
            return line.word
        
        return None

    def get_current_bracket(self) -> Optional[Tuple[int, int, str]]:
        """Get bracket info at current cursor position"""
        line = self.grid_lines[self.cursor_row]
        
        if line.bracket_info and not line.bracket_used:
            bracket_start, bracket_end, bracket_pair = line.bracket_info
            if self.cursor_col == bracket_start:
                return line.bracket_info
        
        return None

    def count_matches(self, word: str) -> int:
        return sum(1 for a, b in zip(word, self.password) if a == b)

    def make_guess(self, word: str) -> bool:
        if self.game_over or self.locked_out:
            return False
        
        # Check if word is a removed dud
        for line in self.grid_lines:
            if line.word == word and line.removed:
                return False
        
        if word not in self.words:
            return False
        
        matches = self.count_matches(word)
        
        self.last_guess = word
        self.last_match_count = matches
        self.attempts_left -= 1
        
        if matches == self.password_length:
            self.output_history.append("ACCESS GRANTED")
            # Keep only last 17 outputs
            self.output_history = self.output_history[-17:]
            self.won = True
            self.game_over = True
            return True
        
        self.output_history.append(word)
        self.output_history.append("Entry denied")
        self.output_history.append(f"{matches}/{self.password_length} correct")
        # Keep only last 17 outputs
        self.output_history = self.output_history[-17:]
        
        if self.attempts_left <= 0 and not self.config['retry']:
            self.locked_out = True
            self.game_over = True
        
        return False

    def activate_bracket(self) -> Tuple[bool, str]:
        if self.game_over or self.locked_out:
            return False, ""
        
        bracket_info = self.get_current_bracket()
        if not bracket_info:
            return False, ""
        
        # Mark bracket as used and replace with periods
        line = self.grid_lines[self.cursor_row]
        bracket_start, bracket_end, bracket_pair = bracket_info
        line.bracket_used = True
        
        # Replace bracket characters with periods
        content_list = list(line.content)
        content_list[bracket_start] = '.'
        content_list[bracket_end] = '.'
        line.content = ''.join(content_list)
        
        # Decide action: remove dud or replenish
        # Only ONE bracket should replenish per puzzle
        if not self.replenish_bracket_used:
            # 50% chance for first bracket, decreasing for others
            non_password_words = [i for i, line in enumerate(self.grid_lines) if line.word and line.word != self.password and not line.removed]
            
            if non_password_words and random.random() < 0.5:
                # Remove dud - replace word with dots
                dud_idx = random.choice(non_password_words)
                dud_line = self.grid_lines[dud_idx]
                word_len = len(dud_line.word)
                
                # Replace word with dots
                content_list = list(dud_line.content)
                for i in range(dud_line.word_start, dud_line.word_start + word_len):
                    content_list[i] = '.'
                dud_line.content = ''.join(content_list)
                dud_line.removed = True
                
                self.output_history.append("Dud removed.")
                # Keep only last 17 outputs
                self.output_history = self.output_history[-17:]
                return True, "Dud removed"
            else:
                # Replenish
                self.replenish_bracket_used = True
                self.attempts_left = self.max_attempts
                self.output_history.append("Attempts reset.")
                # Keep only last 17 outputs
                self.output_history = self.output_history[-17:]
                return True, "Attempts reset"
        else:
            # Only remove duds after replenish used
            non_password_words = [i for i, line in enumerate(self.grid_lines) if line.word and line.word != self.password and not line.removed]
            if non_password_words:
                dud_idx = random.choice(non_password_words)
                dud_line = self.grid_lines[dud_idx]
                word_len = len(dud_line.word)
                
                # Replace word with dots
                content_list = list(dud_line.content)
                for i in range(dud_line.word_start, dud_line.word_start + word_len):
                    content_list[i] = '.'
                dud_line.content = ''.join(content_list)
                dud_line.removed = True
                
                self.output_history.append("Dud removed.")
                # Keep only last 17 outputs
                self.output_history = self.output_history[-17:]
                return True, "Dud removed"
        
        return False, "No action available"


def draw_header(stdscr, game: HackingGame):
    config = DIFFICULTY_CONFIG[game.difficulty]
    
    stdscr.addstr(0, 0, "Robco industries (tm) termlink protocol")
    stdscr.addstr(1, 0, "Enter password now")
    stdscr.addstr(2, 0, "")
    
    # Draw attempts with block characters
    attempts_str = f"{game.attempts_left} attempt(s) left: "
    blocks = "█ " * game.attempts_left
    stdscr.addstr(3, 0, attempts_str + blocks)
    
    stdscr.addstr(4, 0, "")


def draw_grid(stdscr, game: HackingGame, start_row: int):
    num_columns = 2  # Two columns of content
    num_rows = 17
    
    # Draw the 2 columns of content
    for row_idx in range(num_rows):
        row = start_row + row_idx
        
        # Draw up to 2 columns per row
        for col_idx in range(num_columns):
            line_idx = row_idx * num_columns + col_idx
            if line_idx >= len(game.grid_lines):
                break
            
            line = game.grid_lines[line_idx]
            
            # Calculate column position
            col_pos = col_idx * (len(line.address) + len(line.content) + 5)
            
            # Determine highlight range
            if line_idx == game.cursor_row:
                highlight_start, highlight_end = game.get_current_highlight()
            else:
                highlight_start, highlight_end = -1, -1
            
            # Draw address
            try:
                stdscr.addstr(row, col_pos, line.address)
            except curses.error:
                pass
            
            # Draw content with highlighting
            content_col = col_pos + len(line.address) + 1
            for j, char in enumerate(line.content):
                try:
                    if line_idx == game.cursor_row and highlight_start <= j < highlight_end:
                        stdscr.addstr(row, content_col + j, char, curses.A_REVERSE)
                    else:
                        stdscr.addstr(row, content_col + j, char)
                except curses.error:
                    pass
    
    # Draw the output column (third column)
    output_col_start = 2 * (len(game.grid_lines[0].address) + len(game.grid_lines[0].content) + 5)
    
    # Show last 17 outputs, with newest at the bottom
    recent_outputs = game.output_history[-17:] if len(game.output_history) > 17 else game.output_history
    
    for i, output in enumerate(recent_outputs):
        row = start_row + i
        try:
            stdscr.addstr(row, output_col_start, "> " + output)
        except curses.error:
            pass


def draw_final_output(stdscr, game: HackingGame, row: int):
    if game.won:
        stdscr.addstr(row, 0, "ACCESS GRANTED", curses.A_BOLD)
    elif game.locked_out:
        # Center the terminal locked message
        stdscr.addstr(row, 0, "")
        stdscr.addstr(row + 1, 0, "      TERMINAL LOCKED", curses.A_BOLD)
        stdscr.addstr(row + 2, 0, "PLEASE CONTACT ADMINISTRATOR", curses.A_BOLD)


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(0)
    stdscr.clear()
    
    game = HackingGame(args.difficulty)
    
    while not game.game_over:
        stdscr.clear()
        stdscr.refresh()
        
        draw_header(stdscr, game)
        draw_grid(stdscr, game, 5)
        
        stdscr.refresh()
        
        key = stdscr.getch()
        
        if key == ord('q') or key == ord('Q'):
            break
        
        # Navigation
        num_columns = 2
        num_rows = 17
        
        if key == curses.KEY_UP:
            # Move up within current column
            current_row = game.cursor_row // num_columns
            current_col = game.cursor_row % num_columns
            if current_row > 0:
                game.cursor_row = (current_row - 1) * num_columns + current_col
        elif key == curses.KEY_DOWN:
            # Move down within current column
            current_row = game.cursor_row // num_columns
            current_col = game.cursor_row % num_columns
            if current_row < num_rows - 1:
                game.cursor_row = (current_row + 1) * num_columns + current_col
        elif key == curses.KEY_LEFT:
            # Move left within current row
            current_line = game.grid_lines[game.cursor_row]
            if game.cursor_col > 0:
                game.cursor_col -= 1
            else:
                # At first character of row
                current_col = game.cursor_row % num_columns
                current_row = game.cursor_row // num_columns
                
                if current_col == 1:
                    # In column 2, move to last character of column 1 (same row)
                    prev_line_idx = current_row * num_columns
                    if prev_line_idx < len(game.grid_lines):
                        game.cursor_row = prev_line_idx
                        game.cursor_col = len(game.grid_lines[prev_line_idx].content) - 1
                elif current_col == 0 and current_row > 0:
                    # In column 1, move to last character of column 2 (previous row)
                    prev_row = current_row - 1
                    prev_line_idx = prev_row * num_columns + 1
                    if prev_line_idx < len(game.grid_lines):
                        game.cursor_row = prev_line_idx
                        game.cursor_col = len(game.grid_lines[prev_line_idx].content) - 1
        elif key == curses.KEY_RIGHT:
            # Move right within current row
            current_line = game.grid_lines[game.cursor_row]
            if game.cursor_col < len(current_line.content) - 1:
                game.cursor_col += 1
            else:
                # At last character of row
                current_col = game.cursor_row % num_columns
                current_row = game.cursor_row // num_columns
                
                if current_col == 0 and current_row < num_rows - 1:
                    # Move to first character of column 2, same row
                    next_line_idx = current_row * num_columns + 1
                    if next_line_idx < len(game.grid_lines):
                        game.cursor_row = next_line_idx
                        game.cursor_col = 0
                elif current_col == 1:
                    # In column 2, move to first character of column 1, next row
                    next_row = (current_row + 1) % num_rows  # Wrap around to first row if at bottom
                    next_line_idx = next_row * num_columns
                    if next_line_idx < len(game.grid_lines):
                        game.cursor_row = next_line_idx
                        game.cursor_col = 0
        
        # Selection
        elif key == curses.KEY_ENTER or key in [10, 13]:
            # Check if on a word
            current_word = game.get_current_word()
            if current_word:
                game.make_guess(current_word)
            else:
                # Check if on a bracket
                game.activate_bracket()
    
    # Show final state
    stdscr.clear()
    
    if game.locked_out:
        # Blank screen and show terminal locked message
        stdscr.addstr(0, 0, "")
        stdscr.addstr(1, 0, "      TERMINAL LOCKED", curses.A_BOLD)
        stdscr.addstr(2, 0, "PLEASE CONTACT ADMINISTRATOR", curses.A_BOLD)
    else:
        draw_header(stdscr, game)
        draw_grid(stdscr, game, 5)
        
        num_rows = 17
        draw_final_output(stdscr, game, 5 + num_rows + 2)
    
    stdscr.addstr(5 + 17 + 4, 0, "Press any key to exit...")
    stdscr.refresh()
    stdscr.getch()


if __name__ == '__main__':
    # Parse arguments before initializing curses
    parser = argparse.ArgumentParser(
        description='Fallout 4 Hacking Mini-Game',
        add_help=False
    )
    parser.add_argument('-d', '--difficulty', type=int, choices=[1, 2, 3, 4, 5],
                        help='Difficulty level (1-5)')
    parser.add_argument('-h', '--help', action='store_true',
                        help='Display this help file')
    args = parser.parse_args()
    
    # Display help if requested or no difficulty specified
    if args.help or args.difficulty is None:
        print("Syntax: fallout_hacking.py [OPTION]")
        print()
        print("Options are:")
        print("  --difficulty=[1-5]  loads the mini game with the specified difficulty level (-d[1-5])")
        print("  --help             displays this help file")
        print()
        print("Difficulty levels:")
        print("  1 - Very Easy: 4-5 char passwords")
        print()
        print("  2 - Easy: 6-8 char passwords")
        print()
        print("  3 - Average: 9-10 char passwords")
        print()
        print("  4 - Hard: 11-12 char passwords")
        print()
        print("  5 - Very Hard: 13-15 char passwords")
        sys.exit(0)
    
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        sys.exit(0)
