
import loggingfrom telegram import Update, InlineKeyboardButton, 
InlineKeyboardMarkupfrom telegram.ext import ApplicationBuilder, 
CommandHandler, CallbackQueryHandler, ContextTypesimport asyncioimport random
#TOKEN =8333584730:AAGYfKB5b4MQmHJGJmrbaOIZ2baa21WCTSMК
# Настроим логированиеlogging.basicConfig(format='%(asctime)s - %(name)s - 
%(levelname)s - %(message)s', level=logging.INFO)
# Размер игрового поляWIDTH = 10HEIGHT = 20
# Определяем фигуры (только основные для простоты)TETROMINOS = { 'I': [[1, 1, 
1, 1]], 'O': [[1, 1], [1, 1]], 'T': [[0,1,0], [1,1,1]], 'S': [[0,1,1], [1,1,0]],
 'Z': [[1,1,0], [0,1,1]], 'J': [[1,0,0], [1,1,1]], 'L': [[0,0,1], [1,1,1]],}
# Цвета и символы для отображенияFILLED_CELL = '⬛'EMPTY_CELL = '⬜'
# Структура для хранения состояния игрыgames = {}
def generate_empty_board(): return [[0 for _ in range(WIDTH)] for _ in 
range(HEIGHT)]
def rotate(matrix): return [list(row) for row in zip(*matrix[::-1])]
def check_collision(board, shape, offset): off_x, off_y = offset for y, row in 
enumerate(shape): for x, cell in enumerate(row): if cell: new_x = off_x + x 
new_y = off_y + y if new_x < 0 or new_x >= WIDTH or new_y >= HEIGHT: return True
 if new_y >= 0 and board[new_y][new_x]: return True return False
def merge_shape(board, shape, offset): off_x, off_y = offset for y, row in 
enumerate(shape): for x, cell in enumerate(row): if cell and 0 <= off_y + y < 
HEIGHT and 0 <= off_x + x < WIDTH: board[off_y + y][off_x + x] = 1
def remove_full_lines(board): new_board = [row for row in board if any(cell == 
0 for cell in row)] lines_cleared = HEIGHT - len(new_board) for _ in 
range(lines_cleared): new_board.insert(0, [0]*WIDTH) return new_board, 
lines_cleared
async def draw_board(board): display = '' for row in board: for cell in row: 
display += FILLED_CELL if cell else EMPTY_CELL display += '\n' return display
async def start_game(update: Update, context: ContextTypes.DEFAULT_TYPE): 
chat_id = update.effective_chat.id # Создаем новую игру board = 
generate_empty_board() current_piece_type = 
random.choice(list(TETROMINOS.keys())) current_shape = 
TETROMINOS[current_piece_type] current_pos = [WIDTH // 2 - 
len(current_shape[0]) // 2, 0] game_state = { 'board': board, 'current_shape': 
current_shape, 'current_type': current_piece_type, 'pos': current_pos, 'score': 
0, 'game_over': False, } games[chat_id] = game_state
 # Создаем клавиатуру для управления keyboard = [ [ InlineKeyboardButton('⬅️', 
callback_d