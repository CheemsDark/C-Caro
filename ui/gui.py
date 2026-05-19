import pygame
import sys
import threading
import time
import os
from core.game_engine import GameEngine
from core.board import Board
from ai.agent import AIAgent

BG_COLOR = (28, 30, 38)
BOARD_BG = (40, 42, 54)
GRID_COLOR = (98, 114, 164)
TEXT_COLOR = (248, 248, 242)
TEXT_DIM = (180, 180, 180)
BUTTON_BG = (68, 71, 90)
BUTTON_HOVER = (98, 114, 164)
PLAYER_X_COLOR = (255, 85, 85)
PLAYER_O_COLOR = (139, 233, 253)
WIN_LINE_COLOR = (80, 250, 123)

class PygameUI:
    def __init__(self, size=15):
        pygame.init()
        self.size = size
        self.board_pixel_size = 750
        self.dashboard_width = 400
        self.cell_size = self.board_pixel_size // self.size
        self.width = self.board_pixel_size + self.dashboard_width
        self.height = self.board_pixel_size
        
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Caro AI PRO")
        
        self.font_huge = pygame.font.SysFont("segoeui", 64, bold=True)
        self.font_large = pygame.font.SysFont("segoeui", 40, bold=True)
        self.font_medium = pygame.font.SysFont("segoeui", 26, bold=True)
        self.font_small = pygame.font.SysFont("segoeui", 22)
        
        self.state = "MENU"
        self.engine = None
        self.agent_x = None
        self.agent_o = None
        
        self.ai_thinking = False
        self.auto_play_running = False
        self.last_ai_stats_x = None
        self.last_ai_stats_o = None
        self.match_start_time = 0
        self.match_end_time = None
        
        self.difficulty_levels = [("DỄ", 2), ("TRUNG BÌNH", 3), ("KHÓ", 5)]
        self.current_diff_idx = 2 # Default KHÓ
        
        self.btn_pvp = pygame.Rect(self.width//2 - 200, 220, 400, 60)
        self.btn_pva = pygame.Rect(self.width//2 - 200, 300, 400, 60)
        self.btn_pva_ai = pygame.Rect(self.width//2 - 200, 380, 400, 60)
        self.btn_ava = pygame.Rect(self.width//2 - 200, 460, 400, 60)
        
        # Menu Difficulty Buttons
        self.btn_menu_diff_easy = pygame.Rect(self.width//2 - 200, 580, 120, 60)
        self.btn_menu_diff_med = pygame.Rect(self.width//2 - 60, 580, 120, 60)
        self.btn_menu_diff_hard = pygame.Rect(self.width//2 + 80, 580, 120, 60)
        
        # In-game Control Panel
        self.btn_diff_easy = pygame.Rect(self.board_pixel_size + 30, 400, 100, 45)
        self.btn_diff_med = pygame.Rect(self.board_pixel_size + 150, 400, 100, 45)
        self.btn_diff_hard = pygame.Rect(self.board_pixel_size + 270, 400, 100, 45)
        self.btn_restart = pygame.Rect(self.board_pixel_size + 30, 470, 340, 50)
        
        self.btn_quick_pvp = pygame.Rect(self.board_pixel_size + 30, 550, 160, 45)
        self.btn_quick_ava = pygame.Rect(self.board_pixel_size + 210, 550, 160, 45)
        self.btn_quick_pva = pygame.Rect(self.board_pixel_size + 30, 610, 160, 45)
        self.btn_quick_pva_ai = pygame.Rect(self.board_pixel_size + 210, 610, 160, 45)
        
        self.btn_exit = pygame.Rect(self.board_pixel_size + 30, 680, 340, 50)
        self.load_assets()

    def load_assets(self):
        self.images = {}
        assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
        
        def load_img(filename):
            path = os.path.join(assets_dir, filename)
            if os.path.exists(path):
                try:
                    return pygame.image.load(path).convert_alpha()
                except:
                    pass
            return None

        def fit_img(img, max_w, max_h):
            if img is None: return None
            return pygame.transform.smoothscale(img, (max_w, max_h))

        p_size = self.cell_size - 4
        self.images['X'] = fit_img(load_img("X.png"), p_size, p_size)
        self.images['O'] = fit_img(load_img("O.png"), p_size, p_size)
        
        # Helper to load both states
        def load_pair(prefix, normal_file, hover_file, w, h):
            self.images[prefix + '_normal'] = fit_img(load_img(normal_file), w, h)
            self.images[prefix + '_hover'] = fit_img(load_img(hover_file), w, h)

        # Menu Modes (400x60)
        load_pair('menu_pvp', "player_btn.png", "player.png", 400, 60)
        load_pair('menu_pva', "Ai_vs_player_btn.png", "Ai_vs_player.png", 400, 60)
        load_pair('menu_pva_ai', "Ai_vs_player_btn.png", "Ai_vs_player.png", 400, 60)
        load_pair('menu_ava', "AI_btn.png", "AI.png", 400, 60)
        
        # Menu Difficulty (120x60)
        load_pair('menu_E', "E_btn.png", "E.png", 120, 60)
        load_pair('menu_M', "M_btn.png", "M.png", 120, 60)
        load_pair('menu_H', "H_btn.png", "H.png", 120, 60)
        
        # Dash Difficulty (100x45)
        load_pair('dash_E', "E_btn.png", "E.png", 100, 45)
        load_pair('dash_M', "M_btn.png", "M.png", 100, 45)
        load_pair('dash_H', "H_btn.png", "H.png", 100, 45)
        
        # Dash Quick Modes (160x45)
        load_pair('dash_pvp', "player_btn.png", "player.png", 160, 45)
        load_pair('dash_pva', "Ai_vs_player_btn.png", "Ai_vs_player.png", 160, 45)
        load_pair('dash_pva_ai', "Ai_vs_player_btn.png", "Ai_vs_player.png", 160, 45)
        load_pair('dash_ava', "AI_btn.png", "AI.png", 160, 45)
        
        start_img = load_img("start.png")
        self.images['start_normal'] = fit_img(start_img, 340, 50)
        if start_img:
            self.images['start_hover'] = pygame.transform.smoothscale(start_img, (int(340*1.05), int(50*1.05)))

    def draw_menu(self):
        self.screen.fill(BG_COLOR)
        title = self.font_huge.render("CỜ CARO AI", True, TEXT_COLOR)
        self.screen.blit(title, (self.width//2 - title.get_width()//2, 80))
        
        subtitle = self.font_medium.render("Thuật toán Alpha-Beta Tối Ưu (Auto-Depth)", True, PLAYER_O_COLOR)
        self.screen.blit(subtitle, (self.width//2 - subtitle.get_width()//2, 160))
        
        mx, my = pygame.mouse.get_pos()
        
        def draw_menu_btn(rect, img_key_prefix, text, default_color, is_selected=False):
            is_hover = rect.collidepoint((mx, my))
            color = default_color if (is_selected and not is_hover) else (BUTTON_HOVER if is_hover else default_color)
            if is_selected:
                if img_key_prefix == 'menu_E': color = (46, 204, 113)
                elif img_key_prefix == 'menu_M': color = (241, 196, 15)
                elif img_key_prefix == 'menu_H': color = (255, 85, 85)
            
            pygame.draw.rect(self.screen, color, rect, border_radius=8)
            
            use_hover = is_hover or is_selected
            img_key = img_key_prefix + ('_hover' if use_hover else '_normal')
            img = self.images.get(img_key)
            if img is None:
                img = self.images.get(img_key_prefix + '_normal')
                
            if img:
                img_rect = img.get_rect(center=rect.center)
                self.screen.blit(img, img_rect)
            else:
                txt_col = TEXT_COLOR if not (is_selected and img_key_prefix == 'menu_M') else BG_COLOR
                txt_surf = self.font_medium.render(text, True, txt_col)
                self.screen.blit(txt_surf, (rect.x + rect.width//2 - txt_surf.get_width()//2, rect.y + 12))

        draw_menu_btn(self.btn_pvp, 'menu_pvp', "Người vs Người", BUTTON_BG)
        draw_menu_btn(self.btn_pva, 'menu_pva', "Chơi với Máy (Bạn đi trước)", BUTTON_BG)
        draw_menu_btn(self.btn_pva_ai, 'menu_pva_ai', "Chơi với Máy (Máy đi trước)", BUTTON_BG)
        draw_menu_btn(self.btn_ava, 'menu_ava', "Máy vs Máy", BUTTON_BG)
        
        # Menu Difficulty Label
        diff_label = self.font_small.render("Chọn độ khó AI:", True, TEXT_COLOR)
        self.screen.blit(diff_label, (self.width//2 - diff_label.get_width()//2, 540))
        
        draw_menu_btn(self.btn_menu_diff_easy, 'menu_E', "DỄ", BUTTON_BG, self.current_diff_idx == 0)
        draw_menu_btn(self.btn_menu_diff_med, 'menu_M', "TB", BUTTON_BG, self.current_diff_idx == 1)
        draw_menu_btn(self.btn_menu_diff_hard, 'menu_H', "KHÓ", BUTTON_BG, self.current_diff_idx == 2)

    def draw_board(self, board: Board):
        pygame.draw.rect(self.screen, BOARD_BG, (0, 0, self.board_pixel_size, self.board_pixel_size))
        
        for i in range(self.size + 1):
            pygame.draw.line(self.screen, GRID_COLOR, (0, i * self.cell_size), (self.board_pixel_size, i * self.cell_size), 2)
            pygame.draw.line(self.screen, GRID_COLOR, (i * self.cell_size, 0), (i * self.cell_size, self.board_pixel_size), 2)
            
        for r in range(self.size):
            for c in range(self.size):
                center_x = c * self.cell_size + self.cell_size // 2
                center_y = r * self.cell_size + self.cell_size // 2
                
                if board.grid[r][c] == Board.PLAYER_X:
                    if self.images.get('X'):
                        img_rect = self.images['X'].get_rect(center=(center_x, center_y))
                        self.screen.blit(self.images['X'], img_rect)
                    else:
                        offset = self.cell_size // 3
                        pygame.draw.line(self.screen, PLAYER_X_COLOR, (center_x - offset, center_y - offset), (center_x + offset, center_y + offset), 4)
                        pygame.draw.line(self.screen, PLAYER_X_COLOR, (center_x + offset, center_y - offset), (center_x - offset, center_y + offset), 4)
                elif board.grid[r][c] == Board.PLAYER_O:
                    if self.images.get('O'):
                        img_rect = self.images['O'].get_rect(center=(center_x, center_y))
                        self.screen.blit(self.images['O'], img_rect)
                    else:
                        radius = self.cell_size // 3
                        pygame.draw.circle(self.screen, PLAYER_O_COLOR, (center_x, center_y), radius, 4)
                    
        win_x = board.check_win(Board.PLAYER_X)
        win_o = board.check_win(Board.PLAYER_O)
        winning_line = win_x if win_x else win_o
        if isinstance(winning_line, list):
            for r, c in winning_line:
                center_x = c * self.cell_size + self.cell_size // 2
                center_y = r * self.cell_size + self.cell_size // 2
                pygame.draw.circle(self.screen, WIN_LINE_COLOR, (center_x, center_y), self.cell_size // 2 - 4, 3)

    def draw_dashboard(self):
        pygame.draw.rect(self.screen, BG_COLOR, (self.board_pixel_size, 0, self.dashboard_width, self.height))
        
        x_offset = self.board_pixel_size + 30
        y_offset = 20
        
        title = self.font_large.render("CARO AI", True, TEXT_COLOR)
        self.screen.blit(title, (x_offset, y_offset))
        y_offset += 45
        
        status_text = "Đang chơi..."
        color = TEXT_COLOR
        if self.engine.status == "x_won":
            status_text = "BÊN X THẮNG!"
            color = PLAYER_X_COLOR
        elif self.engine.status == "o_won":
            status_text = "BÊN O THẮNG!"
            color = PLAYER_O_COLOR
        elif self.engine.status == "draw":
            status_text = "HÒA NHAU!"
            color = TEXT_DIM
            
        status_surf = self.font_medium.render(status_text, True, color)
        self.screen.blit(status_surf, (x_offset, y_offset))
        y_offset += 35
        
        elapsed = 0
        if self.match_start_time:
            if self.engine.status == "ongoing":
                elapsed = time.time() - self.match_start_time
            else:
                if self.match_end_time is None:
                    self.match_end_time = time.time()
                elapsed = self.match_end_time - self.match_start_time
                
        mins = int(elapsed // 60)
        secs = int(elapsed % 60)
        timer_surf = self.font_medium.render(f"⏱ Thời gian: {mins:02d}:{secs:02d}", True, TEXT_DIM)
        self.screen.blit(timer_surf, (x_offset, y_offset))
        y_offset += 35
        
        if self.ai_thinking:
            think_surf = self.font_medium.render("AI đang suy nghĩ...", True, (241, 250, 140))
            self.screen.blit(think_surf, (x_offset, y_offset))
        y_offset += 35
        
        pygame.draw.line(self.screen, GRID_COLOR, (x_offset, y_offset), (self.width - 30, y_offset), 2)
        y_offset += 20
        
        # In thông số AI (hoặc PvP)
        if self.state in ["PLAYING_PVA", "PLAYING_AVA"]:
            self.screen.blit(self.font_medium.render("Thông số AI:", True, PLAYER_O_COLOR), (x_offset, y_offset))
            y_offset += 35
            if self.last_ai_stats_o:
                self.screen.blit(self.font_small.render(f"Điểm: {self.last_ai_stats_o['score']}", True, TEXT_DIM), (x_offset, y_offset))
                y_offset += 25
                self.screen.blit(self.font_small.render(f"Duyệt: {self.last_ai_stats_o['nodes']:,} nodes", True, TEXT_DIM), (x_offset, y_offset))
                y_offset += 25
                self.screen.blit(self.font_small.render(f"T.gian: {self.last_ai_stats_o['time_ms']:.1f} ms", True, TEXT_DIM), (x_offset, y_offset))
            else:
                self.screen.blit(self.font_small.render("Chưa có dữ liệu", True, TEXT_DIM), (x_offset, y_offset))
            y_offset += 35
            
            if self.state == "PLAYING_AVA":
                self.screen.blit(self.font_medium.render("Thông số MÁY X:", True, PLAYER_X_COLOR), (x_offset, y_offset))
                y_offset += 35
                if self.last_ai_stats_x:
                    self.screen.blit(self.font_small.render(f"Điểm: {self.last_ai_stats_x['score']}", True, TEXT_DIM), (x_offset, y_offset))
                    y_offset += 25
                    self.screen.blit(self.font_small.render(f"Duyệt: {self.last_ai_stats_x['nodes']:,} nodes", True, TEXT_DIM), (x_offset, y_offset))
                    y_offset += 25
                    self.screen.blit(self.font_small.render(f"T.gian: {self.last_ai_stats_x['time_ms']:.1f} ms", True, TEXT_DIM), (x_offset, y_offset))
                else:
                    self.screen.blit(self.font_small.render("Chưa có dữ liệu", True, TEXT_DIM), (x_offset, y_offset))
        elif self.state == "PLAYING_PVP":
            self.screen.blit(self.font_medium.render("Người vs Người", True, PLAYER_X_COLOR), (x_offset, y_offset))
            y_offset += 40
            turn_txt = "Lượt của: X (Đỏ)" if self.engine.current_player == Board.PLAYER_X else "Lượt của: O (Xanh)"
            turn_col = PLAYER_X_COLOR if self.engine.current_player == Board.PLAYER_X else PLAYER_O_COLOR
            self.screen.blit(self.font_medium.render(turn_txt, True, turn_col), (x_offset, y_offset))

        # Control Panel Buttons
        mx, my = pygame.mouse.get_pos()
        
        def draw_dash_btn(rect, img_key_prefix, text, default_color, hover_color, font_type, text_offset, is_selected=False):
            is_hover = rect.collidepoint((mx, my))
            color = hover_color if is_hover else default_color
            if is_selected and not is_hover:
                if img_key_prefix == 'dash_E': color = (46, 204, 113)
                elif img_key_prefix == 'dash_M': color = (241, 196, 15)
                elif img_key_prefix == 'dash_H': color = (255, 85, 85)
            
            pygame.draw.rect(self.screen, color, rect, border_radius=5)
            
            if img_key_prefix:
                use_hover = is_hover or is_selected
                img_key = img_key_prefix + ('_hover' if use_hover else '_normal')
                img = self.images.get(img_key)
                if not img:
                    img = self.images.get(img_key_prefix + '_normal')
                    
                if img:
                    img_rect = img.get_rect(center=rect.center)
                    self.screen.blit(img, img_rect)
                else:
                    txt_col = TEXT_COLOR if not (is_selected and img_key_prefix == 'dash_M') else BG_COLOR
                    txt_surf = font_type.render(text, True, txt_col)
                    self.screen.blit(txt_surf, (rect.x + rect.width//2 - txt_surf.get_width()//2, rect.y + text_offset))
            else:
                txt_col = TEXT_COLOR
                txt_surf = font_type.render(text, True, txt_col)
                self.screen.blit(txt_surf, (rect.x + rect.width//2 - txt_surf.get_width()//2, rect.y + text_offset))

        # 3 Nút Độ Khó (Dashboard)
        draw_dash_btn(self.btn_diff_easy, 'dash_E', "DỄ", BUTTON_BG, BUTTON_HOVER, self.font_small, 7, self.current_diff_idx == 0)
        draw_dash_btn(self.btn_diff_med, 'dash_M', "TB", BUTTON_BG, BUTTON_HOVER, self.font_small, 7, self.current_diff_idx == 1)
        draw_dash_btn(self.btn_diff_hard, 'dash_H', "KHÓ", BUTTON_BG, BUTTON_HOVER, self.font_small, 7, self.current_diff_idx == 2)
        
        # Nút Chơi Lại
        draw_dash_btn(self.btn_restart, 'start', "Chơi Lại Trận Này", (39, 174, 96), (46, 204, 113), self.font_medium, 8)
        
        # 2x2 Grid cho Quick Mode Switch
        draw_dash_btn(self.btn_quick_pvp, 'dash_pvp', "Ng vs Ng", BUTTON_BG, BUTTON_HOVER, self.font_small, 7)
        draw_dash_btn(self.btn_quick_ava, 'dash_ava', "Máy đấu Máy", BUTTON_BG, BUTTON_HOVER, self.font_small, 7)
        draw_dash_btn(self.btn_quick_pva, 'dash_pva', "Bạn đi trước", BUTTON_BG, BUTTON_HOVER, self.font_small, 7)
        draw_dash_btn(self.btn_quick_pva_ai, 'dash_pva_ai', "Máy đi trước", BUTTON_BG, BUTTON_HOVER, self.font_small, 7)
        
        # Nút Thoát Về Menu
        draw_dash_btn(self.btn_exit, None, "Về Menu Chính", (200, 50, 50), (255, 85, 85), self.font_medium, 5)

    def _ai_worker_pva(self, engine_instance):
        self.ai_thinking = True
        if engine_instance is self.engine:
            result = self.engine.make_ai_move()
            if engine_instance is self.engine:
                self.last_ai_stats_o = result
        self.ai_thinking = False

    def _ai_worker_ava(self, engine_instance):
        self.auto_play_running = True
        while self.state == "PLAYING_AVA" and engine_instance is self.engine and self.engine.status == "ongoing":
            self.ai_thinking = True
            if self.engine.current_player == Board.PLAYER_X:
                result = self.agent_x.get_move(self.engine.board.copy())
                if result["move"]:
                    r, c = result["move"]
                    self.engine.board.make_move(r, c, Board.PLAYER_X)
                    self.engine._check_status()
                    if self.engine.status == "ongoing":
                        self.engine.current_player = Board.PLAYER_O
                if engine_instance is self.engine:
                    self.last_ai_stats_x = result
            else:
                result = self.agent_o.get_move(self.engine.board.copy())
                if result["move"]:
                    r, c = result["move"]
                    self.engine.board.make_move(r, c, Board.PLAYER_O)
                    self.engine._check_status()
                    if self.engine.status == "ongoing":
                        self.engine.current_player = Board.PLAYER_X
                if engine_instance is self.engine:
                    self.last_ai_stats_o = result
            self.ai_thinking = False
            time.sleep(0.5) # Để người xem kịp nhìn nước cờ
        self.auto_play_running = False

    def get_current_depth(self):
        return self.difficulty_levels[self.current_diff_idx][1]

    def start(self):
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = "QUIT"
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    
                    depth = self.get_current_depth()
                    
                    if self.state == "MENU":
                        if self.btn_menu_diff_easy.collidepoint((mx, my)):
                            self.current_diff_idx = 0
                        elif self.btn_menu_diff_med.collidepoint((mx, my)):
                            self.current_diff_idx = 1
                        elif self.btn_menu_diff_hard.collidepoint((mx, my)):
                            self.current_diff_idx = 2
                            
                        elif self.btn_pvp.collidepoint((mx, my)):
                            self.state = "PLAYING_PVP"
                            self.engine = GameEngine(size=self.size)
                            self.match_start_time = time.time()
                            self.match_end_time = None
                            
                        elif self.btn_pva.collidepoint((mx, my)):
                            self.state = "PLAYING_PVA"
                            self.engine = GameEngine(size=self.size, ai_algorithm="alpha_beta", ai_depth=depth, ai_player=Board.PLAYER_O, human_player=Board.PLAYER_X)
                            self.last_ai_stats_o = None
                            self.match_start_time = time.time()
                            self.match_end_time = None
                            
                        elif self.btn_pva_ai.collidepoint((mx, my)):
                            self.state = "PLAYING_PVA"
                            self.engine = GameEngine(size=self.size, ai_algorithm="alpha_beta", ai_depth=depth, ai_player=Board.PLAYER_X, human_player=Board.PLAYER_O)
                            self.last_ai_stats_o = None
                            self.match_start_time = time.time()
                            self.match_end_time = None
                            
                        elif self.btn_ava.collidepoint((mx, my)):
                            self.state = "PLAYING_AVA"
                            self.engine = GameEngine(size=self.size)
                            self.agent_x = AIAgent(algorithm="alpha_beta", depth=depth, ai_player=Board.PLAYER_X, human_player=Board.PLAYER_O)
                            self.agent_o = AIAgent(algorithm="alpha_beta", depth=depth, ai_player=Board.PLAYER_O, human_player=Board.PLAYER_X)
                            self.last_ai_stats_x = None
                            self.last_ai_stats_o = None
                            self.match_start_time = time.time()
                            self.match_end_time = None
                            threading.Thread(target=self._ai_worker_ava, args=(self.engine,), daemon=True).start()
                            
                    elif self.state in ["PLAYING_PVA", "PLAYING_AVA", "PLAYING_PVP"]:
                        if self.btn_diff_easy.collidepoint((mx, my)):
                            self.current_diff_idx = 0
                        elif self.btn_diff_med.collidepoint((mx, my)):
                            self.current_diff_idx = 1
                        elif self.btn_diff_hard.collidepoint((mx, my)):
                            self.current_diff_idx = 2
                            
                        elif self.btn_restart.collidepoint((mx, my)):
                            if self.state == "PLAYING_PVA":
                                ai_player = self.engine.ai_player
                                human_player = self.engine.human_player
                                self.engine = GameEngine(size=self.size, ai_algorithm="alpha_beta", ai_depth=depth, ai_player=ai_player, human_player=human_player)
                                self.last_ai_stats_o = None
                                self.last_ai_stats_x = None
                                self.match_start_time = time.time()
                                self.match_end_time = None
                            elif self.state == "PLAYING_AVA":
                                self.engine = GameEngine(size=self.size)
                                self.agent_x = AIAgent(algorithm="alpha_beta", depth=depth, ai_player=Board.PLAYER_X, human_player=Board.PLAYER_O)
                                self.agent_o = AIAgent(algorithm="alpha_beta", depth=depth, ai_player=Board.PLAYER_O, human_player=Board.PLAYER_X)
                                self.last_ai_stats_x = None
                                self.last_ai_stats_o = None
                                self.match_start_time = time.time()
                                self.match_end_time = None
                                threading.Thread(target=self._ai_worker_ava, args=(self.engine,), daemon=True).start()
                            else: # PVP
                                self.engine = GameEngine(size=self.size)
                                self.match_start_time = time.time()
                                self.match_end_time = None
                                
                        elif self.btn_quick_pvp.collidepoint((mx, my)):
                            self.state = "PLAYING_PVP"
                            self.engine = GameEngine(size=self.size)
                            self.last_ai_stats_x = None
                            self.last_ai_stats_o = None
                            self.match_start_time = time.time()
                            self.match_end_time = None
                                
                        elif self.btn_quick_pva.collidepoint((mx, my)):
                            self.state = "PLAYING_PVA"
                            self.engine = GameEngine(size=self.size, ai_algorithm="alpha_beta", ai_depth=depth, ai_player=Board.PLAYER_O, human_player=Board.PLAYER_X)
                            self.last_ai_stats_o = None
                            self.last_ai_stats_x = None
                            self.match_start_time = time.time()
                            self.match_end_time = None
                            
                        elif self.btn_quick_pva_ai.collidepoint((mx, my)):
                            self.state = "PLAYING_PVA"
                            self.engine = GameEngine(size=self.size, ai_algorithm="alpha_beta", ai_depth=depth, ai_player=Board.PLAYER_X, human_player=Board.PLAYER_O)
                            self.last_ai_stats_o = None
                            self.last_ai_stats_x = None
                            self.match_start_time = time.time()
                            self.match_end_time = None
                            
                        elif self.btn_quick_ava.collidepoint((mx, my)):
                            self.state = "PLAYING_AVA"
                            self.engine = GameEngine(size=self.size)
                            self.agent_x = AIAgent(algorithm="alpha_beta", depth=depth, ai_player=Board.PLAYER_X, human_player=Board.PLAYER_O)
                            self.agent_o = AIAgent(algorithm="alpha_beta", depth=depth, ai_player=Board.PLAYER_O, human_player=Board.PLAYER_X)
                            self.last_ai_stats_x = None
                            self.last_ai_stats_o = None
                            self.match_start_time = time.time()
                            self.match_end_time = None
                            threading.Thread(target=self._ai_worker_ava, args=(self.engine,), daemon=True).start()
                            
                        elif self.btn_exit.collidepoint((mx, my)):
                            self.state = "MENU"
                            self.engine = None
                            
                        elif self.state in ["PLAYING_PVA", "PLAYING_PVP"] and not self.ai_thinking and self.engine.status == "ongoing":
                            if mx < self.board_pixel_size and my < self.board_pixel_size:
                                c = mx // self.cell_size
                                r = my // self.cell_size
                                
                                if self.state == "PLAYING_PVP":
                                    current = self.engine.current_player
                                    if self.engine.board.make_move(r, c, current):
                                        self.engine._check_status()
                                        if self.engine.status == "ongoing":
                                            self.engine.current_player = Board.PLAYER_O if current == Board.PLAYER_X else Board.PLAYER_X
                                else: # PLAYING_PVA
                                    if self.engine.current_player == self.engine.human_player:
                                        self.engine.make_human_move(r, c)
            
            # Tự động cho AI đánh nếu đến lượt của nó trong chế độ Player vs AI
            if self.state == "PLAYING_PVA" and not self.ai_thinking and self.engine.status == "ongoing":
                if self.engine.current_player == self.engine.ai_player:
                    threading.Thread(target=self._ai_worker_pva, args=(self.engine,), daemon=True).start()

            if self.state == "MENU":
                self.draw_menu()
            elif self.state in ["PLAYING_PVA", "PLAYING_AVA", "PLAYING_PVP"]:
                self.screen.fill(BG_COLOR)
                self.draw_board(self.engine.board)
                self.draw_dashboard()
                
            pygame.display.update()
            clock.tick(30)
