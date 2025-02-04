from manimlib import *
import random
import time


class Firework(AnimationGroup):
    def __init__(
        self,
        point: np.ndarray | Mobject,
        color: list = [YELLOW, RED],
        line_length: float = 1.5,
        num_lines: int = 17,
        flash_radius: float = 1.5,
        line_stroke_width: float = 5.,
        run_time: float = 1.0,
        rate_func=slow_into,
        **kwargs
    ):
        self.point = point
        self.color = color
        self.line_length = line_length
        self.num_lines = num_lines
        self.flash_radius = flash_radius
        self.line_stroke_width = line_stroke_width

        self.lines = self.create_lines()
        animations = self.create_line_anims()
        super().__init__(
            *animations,
            group=self.lines,
            run_time=run_time,
            rate_func=rate_func,
            **kwargs,
        )

    def create_lines(self) -> VGroup:
        lines = VGroup()
        for angle in np.arange(0, TAU, TAU / self.num_lines):
            line = Line(ORIGIN, self.line_length * RIGHT)
            line.shift((self.flash_radius - self.line_length) * RIGHT)
            line.rotate(angle, about_point=ORIGIN)
            lines.add(line)
        lines.set_stroke(
            color=self.color,
            width=self.line_stroke_width
        )
        lines.add_updater(lambda l: l.move_to(self.point))
        return lines

    def create_line_anims(self) -> list[Animation]:
        return [
            ShowCreationThenDestruction(line)
            for line in self.lines
        ]


class ProjectiveTransform(Scene):
    def transform_1(self, p: list) -> list:
        '''
        射影变换
        '''
        # 避免出现除以 0 的情况
        if p[0] + p[1] + 4 == 0:
            return [10000 * p[0], 10000 * p[1], 0]
        return [
            4 * p[0] / (p[0] + p[1] + 4),
            4 * p[1] / (p[0] + p[1] + 4),
            0
        ]

    def transform_2(self, p: list) -> list:
        '''
        射影变换
        '''
        # 同上
        if p[0] + p[1] + 2 == 0:
            return [10000 * p[0], 10000 * p[1], 0]
        return [
            2 * (p[0] - p[1]) / (p[0] + p[1] + 2),
            - 4 / (p[0] + p[1] + 2),
            0
        ]

    def transform_3(self, p: list) -> list:
        '''
        射影变换
        '''
        # 同上
        if p[1] + 4 == 0:
            return [10000 * p[0], 10000 * p[1], 0]
        return [
            4 * p[0] / (p[1] + 4),
            (2 * p[1] - 8) / (p[1] + 4),
            0
        ]

    def construct(self):
        # 文字通用参数
        kwargs = {
            'font': '霞鹜文楷 GB 屏幕阅读版',
            't2c': {'射影变换': GOLD, '射影几何': BLUE, '射影平面': MAROON, '直线': TEAL,
                    '二次曲线': GREEN, '圆': GREEN, '抛物线': GREEN,
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
            （非退化的）二次曲线也都可以互相转化。
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
        trans_word_1 = Text(
            '''
            众所周知，射影平面中的每一个点\n
            都可以用齐次坐标表示，
            ''',
            **kwargs
        )
        trans_word_2 = Text(
            '''
            而射影变换又恰恰是\n
            对齐次坐标的线性变换
            ''',
            **kwargs
        )
        trans_words = VGroup(
            trans_word_1,
            trans_word_2
        ).arrange(DOWN, buff=0.6)
        trans_word_3 = Text(
            '''
            以此为据，利用 apply_function 方法，\n
            我们可以轻松地将射影变换绘制出来。
            ''',
            t2f={'apply_function': 'Consolas'},
            **kwargs
        )

        self.play(Write(trans_word_1), run_time=2)
        self.wait(0.5)
        self.play(Write(trans_word_2), run_time=1.5)
        self.wait()
        self.play(FadeOut(trans_words))
        self.play(Write(trans_word_3), run_time=2)
        self.wait()

        # 定义受害平面（划）变换平面
        grid = NumberPlane((-16, 16), (-8, 8))
        grid.add_coordinate_labels()
        grid.prepare_for_nonlinear_transform()
        grid_original = grid.copy()
        # grid.insert_n_curves(100) # 发现没什么效果就去掉了
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
            '''怎么样？挺怪的吧？''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        trans_word_7 = Text(
            '''是不是还挺有空间感的？''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        # 渲染之后发现好像没有那么多细线……
        trans_word_8 = Text(
            '''（假装你没看到这些乱飞的细线）''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        trans_word_9 = Text(
            '''（这些细线我也不知道怎么搞的qwq）''',
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
            FadeTransform(trans_word_3, trans_words_2),
            run_time=2
        )
        self.wait()
        self.play(
            grid.animate.apply_function(self.transform_1),
            run_time=5,
        )
        self.wait()
        self.play(FadeTransform(trans_words_2, trans_word_6))
        self.wait()
        self.play(FadeTransform(trans_word_6, trans_word_7))
        self.wait(2)
        self.play(FadeTransform(trans_word_7, trans_word_8))
        self.wait()
        self.play(FadeTransform(trans_word_8, trans_word_9))
        self.wait()
        self.play(FadeTransform(trans_word_9, trans_word_10))
        self.wait(2)
        self.play(FadeTransform(trans_word_10, trans_word_11))
        self.play(grid.animate.restore(), run_time=2)  # 恢复原状
        self.wait()

        # 定义无穷远直线与圆
        line = Line(DOWN * 4, UP * 4 + LEFT * 8, color=YELLOW)
        circle = Circle(stroke_color=YELLOW_C, radius=np.sqrt(8))
        circle.insert_n_curves(1000)  # 复杂变换常用
        group = VGroup(grid, circle, line)
        group.save_state()

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

        # 加入直线与圆的第二次变换，圆变为抛物线
        self.play(
            FadeTransform(trans_word_11, trans_word_12),
            ShowCreation(VGroup(circle, line))
        )
        self.wait()
        self.play(FadeTransform(trans_word_12, trans_word_13))
        self.wait(2)
        self.bring_to_back(group)
        self.play(
            group.animate.apply_function(self.transform_1),
            run_time=5,
        )
        self.wait()
        self.play(
            frame.animate.set_height(16).rotate(PI / 4),
            rate_func=there_and_back_with_pause,
            run_time=3
        )
        self.wait()
        self.play(group.animate.restore(), run_time=2)  # 恢复原状
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
            FadeTransform(trans_word_13, trans_word_14)
        )
        group.save_state()
        self.wait(2)
        self.play(
            group.animate.apply_function(self.transform_1),
            run_time=5,
        )
        self.wait()
        self.play(
            frame.animate.set_height(16).shift(
                RIGHT * 4 + UP * 4).rotate(PI / 4),
            rate_func=there_and_back_with_pause,
            run_time=3
        )
        self.wait()
        self.play(group.animate.restore(), run_time=2)  # 恢复原状
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
            group.animate.apply_function(self.transform_1),
            run_time=5,
        )
        self.wait()
        self.play(
            frame.animate.shift(DL * 2).rotate(PI / 4),
            rate_func=there_and_back_with_pause,
            run_time=3
        )
        self.wait()
        self.play(group.animate.restore(), run_time=2)  # 恢复原状
        self.wait(2)

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

        # 第二种变换，双曲线变圆
        self.play(FadeOut(trans_word_15))
        self.play(Write(trans_word_16), run_time=2)
        self.wait(2)
        self.play(FadeTransform(trans_word_16, trans_word_17))
        self.play(Uncreate(VGroup(circle, line)))
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
            group.animate.apply_function(self.transform_2),
            run_time=5,
        )
        self.wait(2)
        self.play(FadeTransform(trans_word_21, trans_word_22))
        self.wait(1.5)
        self.play(FadeTransform(trans_word_22, trans_word_23))
        self.wait(2)
        self.play(FadeTransform(trans_word_23, trans_word_24))
        self.play(ShowCreationThenFadeOut(circle_ref))
        self.wait(0.5)
        self.play(FadeTransform(trans_word_24, trans_word_25))
        self.wait(2)
        self.play(FadeTransform(trans_word_25, trans_word_26))
        self.wait(2)
        self.play(group.animate.restore(), run_time=2)  # 恢复原状
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
             [0, -2, -8],
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
        trans_word_32 = Text(
            '''看到这里，学过透视的同学们觉不觉得有点熟悉？''',
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
            group.animate.apply_function(self.transform_3),
            run_time=5,
        )
        self.wait(2)
        self.play(FadeTransform(trans_word_30, trans_word_31))
        self.play(ShowCreationThenFadeOut(circle_ref))
        self.wait(2)
        self.play(FadeTransform(trans_word_31, trans_word_32))
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
        self.play(group.animate.restore(), run_time=2)  # 恢复原状
        self.wait()

        # 字幕 7
        ending_word_1 = Text(
            '''可能有人要说了（其实根本没有）''',
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
            '''至于齐次坐标是什么，矩阵和射影变换有什么关系''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        ending_word_12 = Text(
            '''这里我就不多说了''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        ending_word_13 = Text(
            '''感兴趣的同学可以去看泰勒猫的视频''',
            **kwargs
        ).to_edge(UP).set_backstroke(width=5)
        ending_word_14 = Text(
            '''链接我放简介里了''',
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
        self.play(ShowCreation(ellipse))
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
        self.wait(1.5)
        self.play(FadeTransform(ending_word_13, ending_word_14))
        self.wait(3)
        self.play(*[FadeOut(mobj) for mobj in self.get_mobjects()])
        self.wait()


class HappyNewYear(Scene):
    def construct(self):
        random.seed(time.time())
        new_year = Text('值此乙巳新春佳节，在此恭祝大家', font='霞鹜文楷 GB 屏幕阅读版')
        new_year.to_edge(UP).set_color(YELLOW_D)
        happy_new_year = Text('新 年 快 乐', font='霞鹜文楷 GB 屏幕阅读版',
                              font_size=192, weight=BOLD)
        happy_new_year.set_color(YELLOW)
        back_rect = FullScreenRectangle(10, RED)
        word_1 = Text('烟花放个六，新年顺顺溜溜', font='霞鹜文楷 GB 屏幕阅读版')
        word_1.to_edge(UP).set_color(YELLOW_D)
        word_2 = Text('视频连个三，新年平平安安', font='霞鹜文楷 GB 屏幕阅读版')
        word_2.to_edge(UP).set_color(YELLOW_D)
        words = VGroup(word_1, word_2).arrange(DOWN, buff=0.6)
        word = Text(
            '''
            祝各位在新的一年里：\n
            家庭美满和谐，生活平安幸福；\n
            学业天天向上，事业步步高升！
            ''',
            font='霞鹜文楷 GB 屏幕阅读版'
        ).set_color(YELLOW_D)

        self.play(FadeIn(back_rect))
        self.wait(0.5)
        self.play(Write(new_year), run_time=1.5)
        self.wait()
        self.play(Write(happy_new_year), run_time=2.5)
        self.wait()

        xs = [random.random() * 14 - 7 for i in range(6)]
        ys = [random.random() * 4 for i in range(6)]
        position_map = [np.array([x, y, 0]) for x, y in zip(xs, ys)]
        for position in position_map:
            self.play(Firework(position, [RED, YELLOW]))
        self.wait()

        self.play(
            FadeOutToPoint(happy_new_year, ORIGIN),
            FadeOutToPoint(new_year, new_year.get_center())
        )
        self.wait(0.5)
        self.play(GrowFromCenter(word_1))
        self.wait(0.5)
        self.play(GrowFromCenter(word_2))
        self.wait(2)
        self.play(FadeOutToPoint(words, ORIGIN))
        self.wait()
        self.play(Write(word), run_time=3)
        self.wait_until(lambda: self.time > 30.5)


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
