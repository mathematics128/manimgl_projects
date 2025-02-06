from manimlib import *


class ProjectiveTransform(Scene):
    def transform_1(self, p: list, beta: float) -> list:
        '''
        射影变换
        '''
        # 避免出现除以 0 的情况
        if (p[0] + p[1]) * beta / 4 + 1 == 0:
            return [10000 * p[0], 10000 * p[1], 0]
        return [
            p[0] / ((p[0] + p[1]) * beta / 4 + 1),
            p[1] / ((p[0] + p[1]) * beta / 4 + 1),
            0
        ]

    def update_func_1(self, grid: VMobject, alpha: float):
        '''
        更新函数
        '''
        beta = smooth(alpha)
        grid.restore()
        grid.apply_function(lambda p: self.transform_1(p, beta))

    def transform_2(self, p: list, beta: float) -> list:
        '''
        射影变换
        '''
        # 同上
        if (p[0] + p[1]) * beta / 2 + 1 == 0:
            return [10000 * p[0], 10000 * p[1], 0]
        return [
            (p[0] - p[1] * beta) / ((p[0] + p[1]) * beta / 2 + 1),
            (p[1] * (1 - beta) - 2 * beta) / ((p[0] + p[1]) * beta / 2 + 1),
            0
        ]

    def update_func_2(self, grid: VMobject, alpha: float):
        '''
        更新函数
        '''
        beta = smooth(alpha)
        grid.restore()
        grid.apply_function(lambda p: self.transform_2(p, beta))

    def transform_3(self, p: list, beta: float) -> list:
        '''
        射影变换
        '''
        # 同上
        if p[1] * beta / 4 + 1 == 0:
            return [10000 * p[0], 10000 * p[1], 0]
        return [
            p[0] / (p[1] * beta / 4 + 1),
            (p[1] * (1 - beta / 2) - 2 * beta) / (p[1] * beta / 4 + 1),
            0
        ]

    def update_func_3(self, grid: VMobject, alpha: float):
        '''
        更新函数
        '''
        beta = smooth(alpha)
        grid.restore()
        grid.apply_function(lambda p: self.transform_3(p, beta))

    def update_line_1(self, dline: Line, alpha: float):
        '''
        无穷远直线的更新函数
        '''
        beta = smooth(alpha)
        if beta == 0:
            pass
        else:
            dline.put_start_and_end_on(
                np.array([-8 / beta, 12 / beta, 0]),
                np.array([12 / beta, -8 / beta, 0])
            )

    def update_line_2(self, dline: Line, alpha: float):
        '''
        无穷远直线的更新函数
        '''
        beta = smooth(alpha)
        if beta == 0:
            pass
        else:
            dline.put_start_and_end_on(
                np.array([-(3+5*beta)/beta, 5*(1-beta)/beta, 0]),
                np.array([(5+3*beta)/beta, 3*(beta-1)/beta, 0])
            )

    def update_line_3(self, dline: Line, alpha: float):
        '''
        无穷远直线的更新函数
        '''
        beta = smooth(alpha)
        if beta == 0:
            pass
        else:
            dline.put_start_and_end_on(
                np.array([-8, (4 - 2 * beta) / beta, 0]),
                np.array([8, (4 - 2 * beta) / beta, 0])
            )

    def construct(self):
        # 文字通用参数
        kwargs = {
            'font': '霞鹜文楷 GB 屏幕阅读版',
            't2c': {'射影变换': GOLD, '射影几何': BLUE, '射影平面': MAROON, '直线': TEAL,
                    '二次曲线': GREEN, '圆锥曲线': GREEN, '圆': GREEN, '抛物线': GREEN,
                    '双曲线': GREEN, '椭圆': GREEN, 'apply_function': BLUE,
                    '仿射变换': PURPLE, '欧氏变换': PURPLE, '线性变换': PURPLE}
        }
        frame = self.camera.frame

        # 引入词
        introduction_1 = Text(
            '''
            在射影几何中，\n
            射影变换占据了极其核心的位置。
            ''',
            **kwargs
        )
        introduction_2 = Text(
            '''
            在射影变换作用下，直线依然是直线，而所有\n
            （非退化的）圆锥曲线也都可以互相转化。
            ''',
            **kwargs
        )
        introduction_3 = Text(
            '''
            但，除此之外呢？\n
            我们还知道什么呢？
            ''',
            **kwargs
        )
        introduction_4 = Text(
            '''
            射影变换施加在整个平面上，\n
            看上去是什么样的呢？
            ''',
            **kwargs
        )
        introduction_5 = Text(
            '''
            能否像线性变换一样，用动画\n
            把射影变换的样子展现出来呢？
            ''',
            **kwargs
        )
        introduction_5.to_edge(UP, buff=LARGE_BUFF)
        introduction_5.set_backstroke(width=5)
        grid_linear = NumberPlane((-10, 10), (-5, 5))

        self.play(Write(introduction_1), run_time=2)
        self.wait()
        self.play(FadeOut(introduction_1))
        self.play(Write(introduction_2), run_time=3)
        self.wait()
        self.play(FadeOut(introduction_2))
        self.play(Write(introduction_3), run_time=1.5)
        self.wait()
        self.play(FadeOut(introduction_3))
        self.play(Write(introduction_4), run_time=2)
        self.wait(2)
        self.play(
            ShowCreation(grid_linear),
            FadeTransform(introduction_4, introduction_5)
        )
        self.wait()
        self.play(grid_linear.animate.apply_matrix(
            [[2, 1], [1, 2]]), run_time=3)
        self.wait(2)
        self.play(*[FadeOut(mobj) for mobj in self.get_mobjects()])
        self.wait()

        # 字幕 0
        bg_word_1 = Text(
            '''为此，我们需要一些背景知识''',
            **kwargs
        )
        bg_word_2 = Text(
            '''
            射影平面和欧式平面最大的区别\n
            就在于射影平面上存在无穷远点
            ''',
            **kwargs
        )
        bg_word_3 = Text(
            '''
            为了表示无穷远点，\n
            我们引入齐次坐标：
            ''',
            **kwargs
        )
        bg_word_4 = Text(
            '''在一般的坐标基础上增加第三个坐标''',
            **kwargs
        ).to_edge(UP)
        bg_tex_1 = Tex('(x, y', ')', font_size=96)
        bg_tex_2 = Tex('(x, y', ', z', ')', font_size=96)
        bg_word_5 = Text(
            '''并作如下规定：''',
            **kwargs
        ).to_edge(UP)
        bg_tex_3 = Tex(
            r'''
            =
            \begin{cases}
            \left( \dfrac xz , \dfrac yz \right),\ \mathrm{When}\ z \neq 0 \\\\
            \mathrm{Infinite\ point}, \ \mathrm{When}\ z = 0
            \end{cases}
            '''
        )
        bg_word_6 = Text(
            '''这样就可以完美表示普通点和无穷远点了''',
            **kwargs
        ).to_edge(UP)
        bg_word_7 = Text(
            '''并且数学家已经证明''',
            **kwargs
        ).to_edge(UP)
        bg_word_8 = Text(
            '''射影变换就是对齐次坐标的线性变换''',
            **kwargs
        ).to_edge(UP)
        bg_word_9 = Text(
            '''也就是说它可以写成矩阵的形式''',
            **kwargs
        ).to_edge(UP)
        bg_tex_4 = Tex(
            r'''
            \left[ \begin{array}{ccc}
            x' \\ y' \\ z' \\
            \end{array} \right]
            =
            \left[ \begin{array}{ccc}
            a_{11} & a_{12} & a_{13} \\
            a_{21} & a_{22} & a_{33} \\
            a_{31} & a_{32} & a_{33} \\
            \end{array} \right]
            \left[ \begin{array}{ccc}
            x \\ y \\ z \\
            \end{array} \right]
            '''
        )
        bg_word_10 = Text(
            '''这样，我们就可以愉快地绘制射影变换啦''',
            **kwargs
        )

        self.play(Write(bg_word_1))
        self.wait()
        self.play(FadeOut(bg_word_1))
        self.play(Write(bg_word_2), run_time=2)
        self.wait()
        self.play(FadeOut(bg_word_2))
        self.play(Write(bg_word_3))
        self.wait()
        self.play(
            FadeTransform(bg_word_3, bg_word_4),
            Write(bg_tex_1)
        )
        self.wait()
        self.play(TransformMatchingTex(bg_tex_1, bg_tex_2), run_time=1)
        self.wait()
        self.play(FadeTransform(bg_word_4, bg_word_5))
        self.play(bg_tex_2.animate.scale(0.5).shift(LEFT * 3))
        bg_tex_3.next_to(bg_tex_2)
        self.play(Write(bg_tex_3), run_time=2)
        self.wait(2)
        self.play(FadeTransform(bg_word_5, bg_word_6))
        self.wait(2)
        self.play(*[FadeOut(mobj) for mobj in self.get_mobjects()])
        self.play(Write(bg_word_7))
        self.wait(0.5)
        self.play(FadeTransform(bg_word_7, bg_word_8))
        self.wait(1.5)
        self.play(FadeTransform(bg_word_8, bg_word_9))
        self.wait(0.5)
        self.play(Write(bg_tex_4), run_time=2.5)
        self.wait(3)
        self.play(
            FadeOut(bg_tex_4),
            FadeTransform(bg_word_9, bg_word_10)
        )
        self.wait(2)

        # 定义受害平面（划）变换平面
        grid = NumberPlane((-16, 16), (-8, 8))
        grid.add_coordinate_labels()
        grid.prepare_for_nonlinear_transform()
        grid_original = grid.copy()
        grid.save_state()

        # 字幕 1
        trans_word_4 = Text(
            '''下面这个变换，对应的就是''',
            **kwargs
        )
        matrix = IntegerMatrix(
            [[4, 0, 0],
             [0, 4, 0],
             [1, 1, 4]]
        ).scale(0.6)
        trans_word_5 = Text(
            '''这个矩阵''',
            **kwargs
        )
        trans_words_2 = VGroup(trans_word_4, matrix, trans_word_5)
        trans_words_2.arrange().to_edge(UP).set_backstroke(width=5)
        trans_word_6 = Text(
            '''怎么样？挺有空间感的吧？''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        trans_word_7 = Text(
            '''是不是就像一个在空间中旋转的平面？''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        # 修改之后的问题变成了色块……
        trans_word_8 = Text(
            '''（假装你没看到这些乱飞的白色块）''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        trans_word_9 = Text(
            '''（这些色块我也不知道怎么搞的qwq）''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        trans_word_10 = Text(
            '''实际上，计算机正是利用射影变换计算空间场景的''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        trans_word_11 = Text(
            '''让我们再看一遍''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)

        # 第一次变换
        self.play(
            ShowCreation(grid),
            FadeTransform(bg_word_10, trans_words_2),
            run_time=2
        )
        self.wait()
        self.play(
            UpdateFromAlphaFunc(grid, self.update_func_1),
            run_time=4
        )
        self.wait(2)
        self.play(FadeTransform(trans_words_2, trans_word_6))
        self.wait(1)
        self.play(FadeTransform(trans_word_6, trans_word_7))
        self.wait(2)
        self.play(FadeTransform(trans_word_7, trans_word_8))
        self.wait()
        self.play(FadeTransform(trans_word_8, trans_word_9))
        self.wait()
        self.play(FadeTransform(trans_word_9, trans_word_10))
        self.wait(2)
        self.play(FadeTransform(trans_word_10, trans_word_11))
        self.play(FadeOut(grid), run_time=0.5)
        grid.restore()  # 恢复原状
        self.play(FadeIn(grid), run_time=0.5)
        self.bring_to_back(grid)
        self.wait()

        # 定义无穷远直线与圆
        line = Line(DOWN * 4, UP * 4 + LEFT * 8, color=YELLOW)
        circle = Circle(stroke_color=YELLOW_C, radius=np.sqrt(8))
        circle.insert_n_curves(1000)  # 复杂变换常用
        group = VGroup(grid, circle, line)
        group.save_state()
        dline_1 = Line(UP * 100, RIGHT * 100, stroke_color=RED)
        dline_1.save_state()

        # 字幕 2
        trans_word_12 = Text(
            '''这次我们加上一个圆和一条直线''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        trans_word_13 = Text(
            '''
            这条线变换后会变成无穷远直线，\n
            而这个圆与之相切，会变成抛物线
            ''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5).fix_in_frame()
        trans_word_13_1 = Text(
            '''
            另外，画面中的红线是\n
            无穷远直线变换后得到的直线
            ''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)

        # 加入直线与圆的第二次变换，圆变为抛物线
        self.play(
            FadeTransform(trans_word_11, trans_word_12),
            ShowCreation(VGroup(circle, line))
        )
        self.add(dline_1)
        self.bring_to_back(dline_1)
        self.wait()
        self.play(FadeTransform(trans_word_12, trans_word_13))
        self.wait(2)
        self.bring_to_back(group)
        self.play(
            UpdateFromAlphaFunc(group, self.update_func_1),
            UpdateFromAlphaFunc(dline_1, self.update_line_1),
            run_time=4
        )
        self.wait()
        self.play(
            frame.animate.set_height(16).rotate(PI / 4),
            rate_func=there_and_back_with_pause,
            run_time=3
        )
        self.wait()
        self.play(FadeTransform(trans_word_13, trans_word_13_1))
        self.wait(2)
        self.play(FadeOut(VGroup(group, dline_1)), run_time=0.5)
        group.restore()  # 恢复原状
        dline_1.restore()
        self.play(FadeIn(VGroup(group, dline_1)), run_time=0.5)
        self.bring_to_back(group, dline_1)
        self.wait()

        # 字幕 3
        trans_word_14 = Text(
            '''
            而如果这个圆大一些，与直线相交，\n
            那它就会变成双曲线
            ''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5).fix_in_frame()

        # 放大圆的第三次变换，圆变为等轴双曲线
        self.play(
            circle.animate.scale(np.sqrt(2)),
            FadeTransform(trans_word_13_1, trans_word_14)
        )
        group.save_state()
        self.wait(2)
        self.play(
            UpdateFromAlphaFunc(group, self.update_func_1),
            UpdateFromAlphaFunc(dline_1, self.update_line_1),
            run_time=4
        )
        self.wait()
        self.play(
            frame.animate.set_height(16).shift(
                RIGHT * 4 + UP * 4).rotate(PI / 4),
            rate_func=there_and_back_with_pause,
            run_time=3
        )
        self.wait()
        self.play(FadeOut(VGroup(group, dline_1)), run_time=0.5)
        group.restore()  # 恢复原状
        dline_1.restore()
        self.play(FadeIn(VGroup(group, dline_1)), run_time=0.5)
        self.bring_to_back(group, dline_1)
        self.wait()

        # 字幕 4
        trans_word_15 = Text(
            '''
            同样的，如果它小一些，与直线相离，\n
            那它就会变成椭圆
            ''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5).fix_in_frame()

        # 缩小圆的第四次变换，圆变为椭圆
        self.play(
            circle.animate.scale(1 / 2),
            FadeTransform(trans_word_14, trans_word_15)
        )
        group.save_state()
        self.wait(2)
        self.play(
            UpdateFromAlphaFunc(group, self.update_func_1),
            UpdateFromAlphaFunc(dline_1, self.update_line_1),
            run_time=4
        )
        self.wait()
        self.play(
            frame.animate.shift(DL * 2).rotate(PI / 4),
            rate_func=there_and_back_with_pause,
            run_time=3
        )
        self.wait(2)
        self.play(FadeOut(VGroup(group, dline_1)), run_time=0.5)
        group.restore()  # 恢复原状
        dline_1.restore()
        self.play(FadeIn(VGroup(group, dline_1)), run_time=0.5)
        self.bring_to_back(group, dline_1)
        self.wait()

        # 字幕 5
        trans_word_16 = Text(
            '''
            看了这么多次同一个变换\n
            想必你也看腻了吧
            ''',
            font_size=72,
            **kwargs
        ).set_backstroke(width=8)
        trans_word_17 = Text(
            '''现在让我们来换一个变换''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        trans_word_18 = Text(
            '''这个变换的矩阵是''',
            **kwargs
        )
        matrix_2 = IntegerMatrix(
            [[2, -2, 0],
             [0, 0, -4],
             [1, 1, 2]],
        ).scale(0.6)
        trans_words_3 = VGroup(trans_word_18, matrix_2)
        trans_words_3.arrange().to_edge(UP).set_backstroke(width=5)
        trans_word_19 = Text(
            '''同时你将看到一条双曲线被变为圆''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        trans_word_20 = Text(
            '''这条双曲线的方程我已经打出来了''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        trans_word_21 = Text(
            '''请看动画''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        trans_word_22 = Text(
            '''可以看到圆断成了两半''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        trans_word_23 = Text(
            '''这是因为实际绘图中双曲线并不会无限延伸''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        trans_word_24 = Text(
            '''我们可以画一个圆来验证一下它确实是个圆''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        trans_word_24_1 = Text(
            '''
            并且这个圆是和红线相交的\n
            意味着双曲线与无穷远直线相交
            ''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        trans_word_25 = Text(
            '''同时，这个场景有着更强的空间感''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        trans_word_26 = Text(
            '''
            如果把上下看成两个平面，那么\n
            你可以感觉到双曲线在平面上本来的样子
            ''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)

        # 定义那条双曲线和参考圆
        hyperbola_1 = FunctionGraph(lambda x: 1/(x+1)-1, (-16, -1.05, .05))
        hyperbola_2 = FunctionGraph(lambda x: 1/(x+1)-1, (-.95, 16, .05))
        hyperbola = VGroup(hyperbola_1, hyperbola_2).set_color(YELLOW)
        hyperbola_label = Tex('(x+1)(y+1)=1', font_size=40).set_color(YELLOW)
        hyperbola_label.align_to(UR * .2, DL).set_backstroke()
        circle_ref = Circle(radius=2)
        dline_2 = Line(LEFT + UP * 100, RIGHT + UP * 100, stroke_color=RED)
        dline_2.save_state()

        # 第二种变换，双曲线变圆
        self.play(FadeOut(trans_word_15))
        self.play(Write(trans_word_16), run_time=2)
        self.wait(2)
        self.play(FadeTransform(trans_word_16, trans_word_17))
        self.play(Uncreate(VGroup(circle, line, dline_1)))
        grid.become(grid_original)
        self.play(FadeOut(grid, remover=False), rate_func=there_and_back)
        self.bring_to_back(grid)
        self.wait()
        self.play(FadeTransform(trans_word_17, trans_words_3))
        self.wait(2)
        self.play(FadeTransform(trans_words_3, trans_word_19))
        self.play(ShowCreation(hyperbola), run_time=2)
        self.wait(0.5)
        self.play(
            FadeTransform(trans_word_19, trans_word_20),
            Write(hyperbola_label)
        )
        self.wait(2)
        self.play(
            FadeTransform(trans_word_20, trans_word_21),
            FadeOut(hyperbola_label)
        )
        self.wait()
        group = VGroup(grid, hyperbola)
        group.save_state()
        self.play(
            UpdateFromAlphaFunc(group, self.update_func_2),
            UpdateFromAlphaFunc(dline_2, self.update_line_2),
            run_time=6
        )
        self.wait(2)
        self.play(FadeTransform(trans_word_21, trans_word_22))
        self.wait(1.5)
        self.play(FadeTransform(trans_word_22, trans_word_23))
        self.wait(2)
        self.play(FadeTransform(trans_word_23, trans_word_24))
        self.play(ShowCreationThenFadeOut(circle_ref))
        self.wait(0.5)
        self.play(FadeTransform(trans_word_24, trans_word_24_1))
        self.wait(2)
        self.play(FadeTransform(trans_word_24_1, trans_word_25))
        self.wait(2)
        self.play(FadeTransform(trans_word_25, trans_word_26))
        self.wait(2)
        self.play(FadeOut(VGroup(group, dline_2)), run_time=0.5)
        group.restore()  # 恢复原状
        dline_2.restore()
        self.play(FadeIn(VGroup(group, dline_2)), run_time=0.5)
        self.bring_to_back(group, dline_2)
        self.wait()

        # 字幕 6
        trans_word_27 = Text(
            '''接下来再看一个抛物线变圆的''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        trans_word_28 = Text(
            '''它对应的矩阵是''',
            **kwargs
        )
        matrix_3 = IntegerMatrix(
            [[4, 0, 0],
             [0, 2, -8],
             [0, 1, 4]]
        ).scale(0.6)
        trans_words_4 = VGroup(trans_word_28, matrix_3)
        trans_words_4.arrange().to_edge(UP).set_backstroke(width=5)
        trans_word_29 = Text(
            '''抛物线的方程同样写在这里''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        trans_word_30 = Text(
            '''请看动画''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        trans_word_31 = Text(
            '''同样画一个圆来验证一下''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        trans_word_31_1 = Text(
            '''
            并且这个圆和红线相切\n
            意味着抛物线和无穷远直线相切
            ''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        trans_word_31_2 = Text(
            '''
            结合前面几次变换，你应该理解了常说的\n
            “三种圆锥曲线的区别只在于和无穷远直线的位置关系”\n
            的真正含义吧！
            ''',
            **kwargs
        ).add_background_rectangle(BLACK, 0.5)
        trans_word_32 = Text(
            '''另外，学过透视的同学们觉不觉得有点熟悉？''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        trans_word_33 = Text(
            '''“这不就是两点透视和一点透视吗？”''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        trans_word_34 = Text(
            '''是的，透视的底层原理就是射影几何''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        trans_word_35 = Text(
            '''正如我刚才说的''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        trans_word_36 = Text(
            '''人处理透视用的是五大定理三大技法''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        trans_word_37 = Text(
            '''而计算机处理透视用的则是射影几何与射影变换''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        trans_word_38 = Text(
            '''二者在底层是等价的''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        trans_word_38_1 = Text(
            '''
            无穷远直线对应地平线\n
            无穷远点则是地面上直线的灭点
            ''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        trans_word_38_2 = Text(
            '''
            射影变换相当于从俯视抬头后的视角转换\n
            将“平行线的相交点”拉到了有穷远处
            ''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        trans_word_39 = Text(
            '''前两个射影变换对应两点透视''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        trans_word_40 = Text(
            '''而这一个则是典型的一点透视''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        trans_word_41 = Text(
            '''
            抛物线两端趋于平行，平行线灭点相同\n
            正好对应这里圆的两端在 y 轴无穷远点汇合
            ''',
            t2f={'y': 'Latin Modern Roman'},
            t2s={'y': ITALIC},
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        trans_word_41_1 = Text(
            '''之前的双曲线也是同理''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        trans_word_42 = Text(
            '''但我把它们绘制出来根本没有用到透视''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        trans_word_43 = Text(
            '''甚至我本人对透视一窍不通''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        trans_word_44 = Text(
            '''数学，很奇妙吧.jpg''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        trans_word_45 = Text(
            '''不过还要多废话几句的是''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        trans_word_46 = Text(
            '''
            射影变换会把“看不见”的部分映射到\n
            “地平线”（无穷远直线）的另一边（天空）
            ''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5).fix_in_frame()
        trans_word_47 = Text(
            '''但透视法会直接丢弃这一半看不见的部分''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        trans_word_48 = Text(
            '''这是我能找到的二者一点小小的不同''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)

        # 定义那条抛物线
        parabola = FunctionGraph(lambda x: x ** 2 / 4, (-16, 16, .1))
        parabola.set_color(YELLOW)
        parabola_label = Tex('x^2=4y', font_size=40).set_color(YELLOW)
        parabola_label.align_to(DOWN * .2, UP).set_backstroke()
        dline_3 = Line(LEFT + UP * 100, RIGHT + UP * 100, stroke_color=RED)
        dline_3.save_state()

        # 第三种变换，抛物线变圆
        self.play(FadeTransform(trans_word_26, trans_word_27))
        self.play(Uncreate(hyperbola), run_time=2)
        self.play(ShowCreation(parabola))
        self.wait(0.5)
        self.play(FadeTransform(trans_word_27, trans_words_4))
        self.wait(2)
        self.play(FadeTransform(trans_words_4, trans_word_29))
        self.play(Write(parabola_label))
        self.wait(2)
        self.play(
            FadeTransform(trans_word_29, trans_word_30),
            FadeOut(parabola_label)
        )
        self.wait()
        group = VGroup(grid, parabola)
        self.bring_to_back(group)
        group.save_state()
        self.play(
            UpdateFromAlphaFunc(group, self.update_func_3),
            UpdateFromAlphaFunc(dline_3, self.update_line_3),
            run_time=4
        )
        self.wait(2)
        self.play(FadeTransform(trans_word_30, trans_word_31))
        self.play(ShowCreationThenFadeOut(circle_ref))
        self.wait()
        self.play(FadeTransform(trans_word_31, trans_word_31_1))
        self.wait(2)
        self.play(FadeTransform(trans_word_31_1, trans_word_31_2))
        self.wait(5)
        self.play(FadeTransform(trans_word_31_2, trans_word_32))
        self.wait(2)
        self.play(FadeTransform(trans_word_32, trans_word_33))
        self.wait(2)
        self.play(FadeTransform(trans_word_33, trans_word_34))
        self.wait(2)
        self.play(FadeTransform(trans_word_34, trans_word_35))
        self.wait()
        self.play(FadeTransform(trans_word_35, trans_word_36))
        self.wait(2)
        self.play(FadeTransform(trans_word_36, trans_word_37))
        self.wait(2)
        self.play(FadeTransform(trans_word_37, trans_word_38))
        self.wait(1)
        self.play(FadeTransform(trans_word_38, trans_word_38_1))
        line_inf = Line(UL * 2 + LEFT * 6, UR * 2 + RIGHT * 6, color=YELLOW)
        self.bring_to_back(line_inf)
        self.play(ShowCreationThenDestruction(line_inf))
        self.wait(2)
        self.play(FadeTransform(trans_word_38_1, trans_word_38_2))
        self.wait(2.5)
        self.play(FadeTransform(trans_word_38_2, trans_word_39))
        self.wait(2)
        self.play(FadeTransform(trans_word_39, trans_word_40))
        self.wait(2)
        self.play(FadeTransform(trans_word_40, trans_word_41))
        self.wait(3.5)
        self.play(FadeTransform(trans_word_41, trans_word_41_1))
        self.wait(1.5)
        self.play(FadeTransform(trans_word_41_1, trans_word_42))
        self.wait(1.5)
        self.play(FadeTransform(trans_word_42, trans_word_43))
        self.wait(1.5)
        self.play(FadeTransform(trans_word_43, trans_word_44))
        self.wait(2)
        self.play(FadeTransform(trans_word_44, trans_word_45))
        self.wait()
        self.play(FadeTransform(trans_word_45, trans_word_46))
        self.play(
            frame.animate.shift(UP * 6),
            rate_func=there_and_back_with_pause,
            run_time=3
        )
        self.wait(0.5)
        self.play(FadeTransform(trans_word_46, trans_word_47))
        self.wait(2.5)
        self.play(FadeTransform(trans_word_47, trans_word_48))
        self.wait(2)
        self.play(FadeOut(VGroup(group, dline_3)), run_time=0.5)
        group.restore()  # 恢复原状
        dline_3.restore()
        self.play(FadeIn(VGroup(group, dline_3)), run_time=0.5)
        self.bring_to_back(group, dline_3)
        self.wait()

        # 字幕 7
        ending_word_1 = Text(
            '''可能有人要说了''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        ending_word_2 = Text(
            '''“主播主播，你的射影变换是很强势''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        ending_word_3 = Text(
            '''“可是你还没有展示椭圆变成圆的变换欸”''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        ending_word_4 = Text(
            '''嘶……这个真的有必要吗……''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        ending_word_5 = Text(
            '''这么平凡的变换也要动用射影吗……''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        ending_word_6 = Text(
            '''罢了，随便放个线性变换吧''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        ending_word_7 = Text(
            '''实在做不动了……''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        ending_word_8 = Text(
            '''
            借此机会，还可以补一句\n
            仿射变换、欧氏变换这些都是射影变换的子集
            ''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        ending_word_9 = Text(
            '''都可以用某些特殊的三阶方阵来表达''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        ending_word_10 = Text(
            '''射影变换则是一般的三阶方阵''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        ending_word_11 = Text(
            '''至于哪些方阵对应仿射变换，哪些对应欧氏变换''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        ending_word_12 = Text(
            '''这里我就不多说了''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        ending_word_13 = Text(
            '''感兴趣的同学可以自己推导一下''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        ending_word_14 = Text(
            '''另外，有了齐次坐标的工具之后''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        ending_word_15 = Text(
            '''
            我们也可以从代数的角度说明\n
            二次曲线射影变换后仍是二次曲线
            ''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        ending_word_16 = Text(
            '''只要把二次曲线的表达式写成二次型就好了''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        ending_word_17 = Text(
            '''留作习题，读者自证不难（''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)

        # 第四种变换（凑数的）
        ellipse = Ellipse(4, 2).set_color(YELLOW)
        self.play(FadeTransform(trans_word_48, ending_word_1))
        self.wait()
        self.play(FadeTransform(ending_word_1, ending_word_2))
        self.wait(1.5)
        self.play(FadeTransform(ending_word_2, ending_word_3))
        self.wait(1.5)
        self.play(FadeTransform(ending_word_3, ending_word_4))
        self.wait()
        self.play(FadeTransform(ending_word_4, ending_word_5))
        self.wait(1.5)
        self.play(FadeTransform(ending_word_5, ending_word_6))
        self.wait(1.5)
        self.play(FadeTransform(ending_word_6, ending_word_7))
        self.play(Uncreate(parabola))
        self.play(ShowCreation(ellipse), run_time=0.5)
        self.wait(0.5)
        group = VGroup(grid, ellipse)
        self.bring_to_back(group)
        self.play(group.animate.apply_matrix([[1, 0], [0, 2]]), run_time=2)
        self.wait()
        self.play(FadeTransform(ending_word_7, ending_word_8))
        self.wait(2.5)
        self.play(FadeTransform(ending_word_8, ending_word_9))
        self.wait(2)
        self.play(FadeTransform(ending_word_9, ending_word_10))
        self.wait(2)
        self.play(FadeTransform(ending_word_10, ending_word_11))
        self.wait(2)
        self.play(FadeTransform(ending_word_11, ending_word_12))
        self.wait()
        self.play(FadeTransform(ending_word_12, ending_word_13))
        self.wait(2)
        self.play(FadeTransform(ending_word_13, ending_word_14))
        self.wait()
        self.play(FadeTransform(ending_word_14, ending_word_15))
        self.wait(2)
        self.play(FadeTransform(ending_word_15, ending_word_16))
        self.wait(2)
        self.play(FadeTransform(ending_word_16, ending_word_17))
        self.wait(3)
        self.play(*[FadeOut(mobj) for mobj in self.get_mobjects()])
        self.wait()


class Cover(Scene):
    def transform(self, p: list) -> list:
        if p[0] + p[1] + 4 == 0:
            return [10000 * p[0], 10000 * p[1], 0]
        return [
            4 * p[0] / (p[0] + p[1] + 4),
            4 * p[1] / (p[0] + p[1] + 4),
            0
        ]

    def construct(self):
        grid = NumberPlane((-16, 16), (-8, 8)).set_stroke(width=5)
        grid.add_coordinate_labels(font_size=48)
        grid.prepare_for_nonlinear_transform()
        circle = Circle(radius=2).set_stroke(YELLOW, 10)
        circle.insert_n_curves(1000)
        group = VGroup(grid, circle)
        group.apply_function(self.transform)
        self.add(group)

        title_1 = Text('射', font='霞鹜文楷 GB 屏幕阅读版', font_size=216)
        title_2 = Text('影', font='霞鹜文楷 GB 屏幕阅读版', font_size=216)
        title_3 = Text('变', font='霞鹜文楷 GB 屏幕阅读版', font_size=216)
        title_4 = Text('换', font='霞鹜文楷 GB 屏幕阅读版', font_size=216)
        title = VGroup(title_1, title_2, title_3, title_4)
        title.arrange(buff=MED_LARGE_BUFF)
        title.set_backstroke(width=20)
        self.add(title)


class Acknowledgement(Scene):
    def construct(self):
        kw = {'font': '霞鹜文楷 GB 屏幕阅读版'}
        text_1 = Text('''
                      非常感谢各位能看到这里！\n
                      也非常感谢漫士的认可，邀请我共同投稿！
                      ''', **kw)
        text_2 = Text('''
                      这一期视频本来没打算参加MaExpo的\n
                      （因为我一开始根本不知道lol）\n
                      所以就自己先发了
                      ''', **kw)
        text_3 = Text('后来有评论告诉我我在公示名单了', **kw)
        text_4 = Text('当时给我激动得啊', **kw)
        text_5 = Text('马上瞌睡全无，起草视频优化方案', **kw)
        text_6 = Text('''
                      因为这期视频我本来没有打磨到底，\n
                      有很多地方都可以改进\n
                      但是由于太懒+电脑性能太差\n
                      就咕咕咕了~(‾▾‾~)
                      ''', **kw)
        text_7 = Text('''
                      后来接到联合投稿邀请，但是电磁力等级不够，\n
                      没法在Up主是我的情况下联合他人投稿\n
                      就索性修改了一遍视频再重新发布
                      ''', **kw)
        text_8 = Text('''
                      主要变化就是改变了变换的动画，\n
                      让它看起来更像是空间旋转\n
                      以及增加了一小段介绍齐次坐标的内容、\n
                      用红线画出了无穷远直线、微调字幕等等
                      ''', **kw)
        text_9 = Text('''
                      源代码也同步发布了\n
                      大家可以在我的Github仓库上查看
                      ''', **kw)
        text_10 = Text('''
                       最后，再次感谢漫士举办的MaExpo比赛！\n
                       这对于小科普Up们是很好的机会与平台！
                       ''', **kw)
        text_11 = Text('''
                       祝MaExpo越办越好！办出SoME的规模！\n
                       祝国内数学科普蒸蒸日上！\n
                       祝屏幕前的各位天天有这样的好视频看！（逃
                       ''', **kw)

        self.play(Write(text_1), run_time=3)
        self.wait()
        self.play(FadeOut(text_1), run_time=0.5)
        self.play(Write(text_2), run_time=3)
        self.wait()
        self.play(FadeOut(text_2), run_time=0.5)
        self.play(Write(text_3), run_time=2)
        self.wait(2)
        self.play(FadeOut(text_3), run_time=0.5)
        self.play(Write(text_4), run_time=1.5)
        self.wait(0.5)
        self.play(ReplacementTransform(text_4, text_5))
        self.wait(2)
        self.play(FadeOut(text_5), run_time=0.5)
        self.play(Write(text_6), run_time=4)
        self.wait(2)
        self.play(FadeOut(text_6), run_time=0.5)
        self.play(Write(text_7), run_time=4)
        self.wait(2)
        self.play(FadeOut(text_7), run_time=0.5)
        self.play(Write(text_8), run_time=4)
        self.wait(3)
        self.play(FadeOut(text_8), run_time=0.5)
        self.play(Write(text_9), run_time=3)
        self.wait()
        self.play(FadeOut(text_9), run_time=0.5)
        self.play(Write(text_10), run_time=3)
        self.wait(2)
        self.play(FadeOut(text_10), run_time=0.5)
        self.play(Write(text_11), run_time=4)
        self.wait(2)
        self.play(FadeOut(text_11), run_time=0.5)
        self.wait()
