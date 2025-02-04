from manimlib import *
import colorsys


class Title(Scene):
    def construct(self):
        def gene_label(
            label: str,
            slant: str = ITALIC,
            size: float = 36,
            color=WHITE
        ) -> Text:
            return Text(
                label, color=color, slant=slant, font_size=size
            ).set_backstroke()

        axes = Axes(x_range=(0, 2.5), y_range=(0, 6), unit_size=0.8)
        coord_a = axes.c2p(2, math.sqrt(32))
        coord_b = axes.c2p(0, 0)
        coord_c = axes.c2p(2, 0)
        coord_d = axes.c2p(2, math.sqrt(2))
        dot_b = Dot(coord_b, fill_color=BLUE_C)
        dot_a = Dot(coord_a, fill_color=BLUE_C)
        dot_c = Dot(coord_c, fill_color=BLUE_C)
        dot_d = Dot(coord_d, fill_color=BLUE_C)
        label_a = gene_label("A")
        label_b = gene_label("B")
        label_c = gene_label("C")
        label_d = gene_label("D")
        label_a.next_to(dot_a, UP)
        label_b.next_to(dot_b, DOWN)
        label_c.next_to(dot_c, DOWN)
        label_d.next_to(dot_d, RIGHT)
        triangle_abc = Polygon(coord_a, coord_b, coord_c)
        triangle_abc.set_stroke(BLUE_C)
        rectangle = Square(0.24)
        rectangle.set_stroke(BLUE_C, width=2)
        rectangle.set_fill(BLUE_C, opacity=0.25)
        rectangle.move_to(axes.c2p(1.85, 0.15))
        segment_cd = Line(coord_c, coord_d, color=YELLOW)
        segment_cd.set_opacity(0.5)
        length_cd = Tex(r"\sqrt{2}", font_size=36)
        length_cd.next_to(segment_cd)
        vertices = VGroup(dot_a, dot_b, dot_c, label_a, label_b, label_c)

        self.wait()
        self.play(ShowCreation(triangle_abc))
        self.play(*[Write(mob) for mob in vertices], run_time=1)
        self.wait()
        self.play(Write(rectangle), run_time=1)
        self.wait()
        self.play(Write(VGroup(dot_d, label_d)), run_time=1)
        self.wait()
        self.play(
            ShowCreationThenFadeOut(segment_cd),
            Write(length_cd), run_time=1
        )
        self.wait()

        dot_p = Dot(fill_color=BLUE_C)
        label_p = gene_label("P")
        dot_p.move_to(axes.c2p(1, 0))
        always(label_p.next_to, dot_p, UL, buff=0.1)
        arrow = Arrow(axes.c2p(1.6, -0.4), axes.c2p(0.4, -0.4), buff=0)
        speed = Tex(r"1\cdot s^{-1}", font_size=32).next_to(arrow, DOWN)

        self.play(FadeIn(VGroup(dot_p, label_p), scale=0.5))
        self.wait(0.5)
        self.play(dot_p.animate.move_to(coord_c))
        self.play(GrowArrow(arrow), Write(speed), run_time=0.75)
        self.play(
            MoveAlongPath(dot_p, Line(coord_c, coord_b)), run_time=2, rate_func=linear
        )
        self.play(
            MoveAlongPath(dot_p, Line(coord_b, coord_a)), run_time=6, rate_func=linear
        )
        self.wait()
        self.play(
            MoveAlongPath(dot_p, Line(coord_a, coord_b)), run_time=0.3, rate_func=rush_into
        )
        self.play(
            MoveAlongPath(dot_p, Line(coord_b, coord_c)), run_time=0.1, rate_func=rush_from
        )
        self.wait()

        t = ValueTracker()

        def p_on_bc():
            f_always(dot_p.move_to, lambda: axes.c2p(2 - t.get_value(), 0))

        def p_on_ab():
            f_always(dot_p.move_to, lambda: axes.c2p(
                     1 / 3 * (t.get_value() - 2),
                     math.sqrt(8 / 9) * (t.get_value() - 2)))

        p_on_bc()
        dot_e = Dot(fill_color=BLUE_C)
        dot_f = Dot(fill_color=BLUE_C)
        label_e = gene_label("E")
        label_f = gene_label("F")
        def p_x(): return axes.p2c(dot_p.get_center())[0]
        def p_y(): return axes.p2c(dot_p.get_center())[1]
        f_always(dot_e.move_to, lambda: axes.c2p(
            p_x()+p_y()-math.sqrt(2), p_y()-p_x()+2))
        f_always(dot_f.move_to, lambda: axes.c2p(
            p_y()+2-math.sqrt(2), math.sqrt(2)-p_x()+2))
        always(label_e.next_to, dot_e, UL, buff=0.1)
        always(label_f.next_to, dot_f, UL, buff=0.1)

        def dpef(): return Polygon(
            coord_d, dot_p.get_center(),
            dot_e.get_center(), dot_f.get_center()
        ).set_fill(BLUE_C, opacity=0.5).set_stroke(BLUE_C)
        sq_dpef = dpef()
        square_dpef = always_redraw(dpef)
        vertices2 = VGroup(dot_e, dot_f, label_e, label_f)

        text1, number1 = t_value = VGroup(
            Text("t = ", slant=ITALIC, t2c=dict(t=YELLOW)),
            DecimalNumber(0, color=BLUE, num_decimal_places=4)
        ).arrange(RIGHT).move_to(UP*0.5+LEFT*5)
        f_always(number1.set_value, t.get_value)

        def dis(x1, x2, y1, y2): return (x1-x2)**2 + (y1-y2)**2
        text2, number2 = s_value = VGroup(
            Text("S = ", slant=ITALIC, t2c=dict(S=YELLOW)),
            DecimalNumber(0, color=BLUE, num_decimal_places=4)
        ).arrange(RIGHT).move_to(DOWN*0.5+LEFT*5)
        f_always(number2.set_value,
                 lambda: dis(p_x(), 2, p_y(), math.sqrt(2)))

        s_label = gene_label("S", size=54, color=YELLOW)
        always(s_label.move_to, square_dpef)

        self.bring_to_back(sq_dpef)
        self.play(
            *[Write(mob) for mob in vertices2],
            ShowCreation(sq_dpef), run_time=0.75
        )
        self.wait()
        self.play(Write(t_value))
        self.wait()
        self.play(Write(s_label))
        self.play(Write(s_value))
        self.wait()
        self.remove(sq_dpef)
        self.add(square_dpef)
        self.bring_to_back(square_dpef)
        self.play(t.animate.set_value(2), run_time=2, rate_func=linear)
        p_on_ab()
        self.play(t.animate.set_value(8), run_time=6, rate_func=linear)
        self.wait()

        question = Text("?", color=RED).move_to(LEFT*5)
        self.play(Write(question), run_time=1)
        self.play(Indicate(question))
        self.wait(3)


class Manim(Scene):
    def construct(self):
        kw = {"font_size": 96, "weight": NORMAL}
        mathe = Text("Mathematical", color=BLUE, **kw)
        anima = Text("Animation", color=RED, **kw)
        VGroup(mathe, anima).arrange(DOWN, buff=0.5)
        self.play(Write(VGroup(mathe, anima)))
        self.wait()
        ma = Text("Ma", t2c={"M": BLUE, "a": "#b655ee"}, **kw)
        anim = Text("anim", t2c={"a": "#b655ee", "nim": RED}, **kw)
        manim = Text(
            "Manim", t2c={"M": BLUE, "a": "#b655ee", "nim": RED}, **kw)
        ma.align_to(manim, DL)
        anim.align_to(manim, UR)
        self.play(
            ReplacementTransform(mathe, ma),
            ReplacementTransform(anima, anim)
        )
        self.wait()
        self.add(manim)
        self.remove(ma, anim)
        self.play(manim.animate.set_color(WHITE), run_time=0.5)
        self.play(manim.animate.set_color_by_gradient(
            BLUE_D, RED_D), run_time=0.5)
        self.wait(3)


class Problem1(Scene):
    def construct(self):
        def gene_label(
            label: str,
            slant: str = ITALIC,
            size: float = 36,
            color=WHITE
        ) -> Text:
            return Text(
                label, color=color, slant=slant, font_size=size
            ).set_backstroke()

        axes = Axes(x_range=(0, 2.5), y_range=(0, 6), unit_size=0.8)
        coord_a = axes.c2p(2, math.sqrt(32))
        coord_b = axes.c2p(0, 0)
        coord_c = axes.c2p(2, 0)
        coord_d = axes.c2p(2, math.sqrt(2))
        dot_b = Dot(coord_b, fill_color=BLUE_C)
        dot_a = Dot(coord_a, fill_color=BLUE_C)
        dot_c = Dot(coord_c, fill_color=BLUE_C)
        dot_d = Dot(coord_d, fill_color=BLUE_C)
        label_a = gene_label("A")
        label_b = gene_label("B")
        label_c = gene_label("C")
        label_d = gene_label("D")
        label_a.next_to(dot_a, UP)
        label_b.next_to(dot_b, DOWN)
        label_c.next_to(dot_c, DOWN)
        label_d.next_to(dot_d, RIGHT)
        triangle_abc = Polygon(coord_a, coord_b, coord_c)
        triangle_abc.set_stroke(BLUE_C)
        rectangle = Square(0.24)
        rectangle.set_stroke(BLUE_C, width=2)
        rectangle.set_fill(BLUE_C, opacity=0.25)
        rectangle.move_to(axes.c2p(1.85, 0.15))
        segment_cd = Line(coord_c, coord_d, color=YELLOW)
        segment_cd.set_opacity(0.5)
        length_cd = Tex(r"\sqrt{2}", font_size=36)
        length_cd.next_to(segment_cd)

        dot_p = Dot(fill_color=BLUE_C)
        label_p = gene_label("P")
        dot_p.move_to(axes.c2p(1, 0))
        always(label_p.next_to, dot_p, UL, buff=0.1)
        arrow = Arrow(axes.c2p(1.6, -0.4), axes.c2p(0.4, -0.4), buff=0)
        speed = Tex(r"1\cdot s^{-1}", font_size=32).next_to(arrow, DOWN)

        t = ValueTracker()

        def p_on_bc():
            f_always(dot_p.move_to, lambda: axes.c2p(2 - t.get_value(), 0))

        def p_on_ab():
            f_always(dot_p.move_to, lambda: axes.c2p(
                     1 / 3 * (t.get_value() - 2),
                     math.sqrt(8 / 9) * (t.get_value() - 2)))

        p_on_bc()
        dot_e = Dot(fill_color=BLUE_C)
        dot_f = Dot(fill_color=BLUE_C)
        label_e = gene_label("E")
        label_f = gene_label("F")
        def p_x(): return axes.p2c(dot_p.get_center())[0]
        def p_y(): return axes.p2c(dot_p.get_center())[1]
        f_always(dot_e.move_to, lambda: axes.c2p(
            p_x()+p_y()-math.sqrt(2), p_y()-p_x()+2))
        f_always(dot_f.move_to, lambda: axes.c2p(
            p_y()+2-math.sqrt(2), math.sqrt(2)-p_x()+2))
        always(label_e.next_to, dot_e, UL, buff=0.1)
        always(label_f.next_to, dot_f, UL, buff=0.1)

        def dpef(): return Polygon(
            coord_d, dot_p.get_center(),
            dot_e.get_center(), dot_f.get_center()
        ).set_fill(BLUE_C, opacity=0.5).set_stroke(BLUE_C)
        square_dpef = always_redraw(dpef)

        s_label = gene_label("S", size=54, color=YELLOW)
        always(s_label.move_to, square_dpef)

        text1, number1 = t_value = VGroup(
            Text("t = ", slant=ITALIC, t2c=dict(t=YELLOW)),
            DecimalNumber(0, color=BLUE, num_decimal_places=4)
        ).arrange(RIGHT)
        f_always(number1.set_value, t.get_value)

        s_value = Text(
            "S = 3", t2c={"S": YELLOW, "3": BLUE},
            t2s={"S": ITALIC}, isolate=["S = ", "3"])
        s_how_many = Text(
            "S = ?", t2c={"S": YELLOW, "?": RED},
            t2s={"S": ITALIC}, isolate=["S = ", "?"])
        what_relation = Tex(
            "S = ? (t)", t2c={"S": YELLOW, "t": YELLOW, "?": BLUE})
        VGroup(t_value, s_value).arrange(DOWN).to_corner(UL, buff=0.75)
        VGroup(t_value, s_how_many).arrange(DOWN).to_corner(UL, buff=0.75)
        s_value.align_to(t_value, LEFT)
        s_how_many.align_to(t_value, LEFT)
        what_relation.next_to(s_value, DOWN, buff=0.5).align_to(t_value, LEFT)

        self.add(rectangle, label_a, label_b, label_c, label_d,
                 dot_a, dot_b, dot_c, dot_d, triangle_abc,
                 dot_p, dot_e, dot_f, label_p, label_e, label_f,
                 square_dpef, s_label, t_value)
        self.bring_to_back(square_dpef)
        self.wait()
        self.play(t.animate.set_value(2), run_time=2, rate_func=linear)
        self.wait()
        self.play(t.animate.set_value(0), run_time=0.2)
        self.wait(0.5)
        self.play(t.animate.set_value(1), run_time=1, rate_func=linear)
        self.wait()
        self.play(Write(s_how_many))
        self.wait()
        self.play(Write(what_relation))
        self.wait(3)
        self.play(FadeOut(what_relation))

        cp_how_many = Tex("CP = t", t2c=dict(CD=YELLOW, t=YELLOW))
        cp_value = Tex("CP = 1", t2c=dict(CD=YELLOW))
        segment_cp = Line(coord_c, dot_p.get_center(), color=YELLOW)
        triangel_dcp = Polygon(
            coord_d, coord_c, dot_p.get_center()
        ).set_stroke(YELLOW).set_fill(YELLOW, opacity=0.5)
        dp_square1 = Tex("DP^2=CP^2+CD^2",
                         t2c={"DP": YELLOW, "CP": YELLOW, "CD": YELLOW})
        dp_square2 = Tex("DP^2=1^2+{(\\sqrt{2})}^2", t2c={"DP": YELLOW})
        dp_square3 = Tex("DP^2=1+2", t2c={"DP": YELLOW})
        dp_square4 = Tex("DP^2=3", t2c={"DP": YELLOW})
        segment_dp = Line(coord_d, dot_p.get_center(),
                          color=YELLOW)
        dp_square5 = Tex("S=3", t2c={"S": YELLOW})

        cp_how_many.next_to(s_value, DOWN, buff=0.5).align_to(t_value, LEFT)
        cp_value.next_to(s_value, DOWN, buff=0.5).align_to(t_value, LEFT)
        dp_square1.to_edge(LEFT, buff=0.75)
        dp_square2.to_edge(LEFT, buff=0.75)
        dp_square3.to_edge(LEFT, buff=0.75)
        dp_square4.to_edge(LEFT, buff=0.75)
        dp_square5.to_edge(LEFT, buff=0.75)

        self.wait()
        self.play(FadeIn(VGroup(arrow, speed)))
        self.wait(10)
        self.play(ShowCreationThenDestruction(segment_cp))
        self.wait(2)
        self.play(Write(cp_how_many))
        self.wait()
        self.play(ShowPassingFlashAround(t_value))
        self.wait(0.5)
        self.play(TransformMatchingTex(cp_how_many, cp_value), run_time=1)
        self.wait()
        self.play(FadeIn(length_cd))
        self.wait()
        self.play(ShowCreationThenFadeOut(triangel_dcp))
        self.wait()
        self.play(Write(dp_square1))
        self.wait()
        self.play(TransformMatchingTex(
            dp_square1, dp_square2,
            key_map={"CP": "1", "CD": "{(\\sqrt{2})}"}), run_time=0.5)
        self.wait(0.5)
        self.play(TransformMatchingTex(
            dp_square2, dp_square3,
            key_map={"1^2": "1", "{(\\sqrt{2})}^2": "2"}),
            run_time=0.5)
        self.wait(0.5)
        self.play(TransformMatchingTex(
            dp_square3, dp_square4,
            key_map={"1+2": "3"}),
            run_time=0.5)
        self.wait()
        self.play(ShowCreationThenDestruction(segment_dp))
        self.wait(2)
        self.play(TransformMatchingTex(
            dp_square4, dp_square5,
            key_map={"DP^2=": "S"}),
            run_time=1)
        self.wait()
        self.play(TransformMatchingStrings(s_how_many, s_value), run_time=1)
        self.play(FadeOut(VGroup(dp_square5, cp_value)))
        self.wait(3)

        dp_square6 = Tex("S=t^2+2", t2c={"S": YELLOW, "t": YELLOW})
        dp_square6.to_edge(LEFT, buff=0.75)
        dp_square1 = Tex("DP^2=CP^2+CD^2",
                         t2c={"DP": YELLOW, "CP": YELLOW, "CD": YELLOW})
        dp_square1.to_edge(LEFT, buff=0.75)

        self.play(Write(cp_how_many))
        self.wait()
        self.play(Write(dp_square1))
        self.wait()
        self.play(TransformMatchingTex(
            dp_square1, dp_square6,
            key_map={"DP^2": "S", "CP": "t", "CD^2": "2"}),
            run_time=1)
        self.wait()
        self.play(
            dp_square6.animate.next_to(s_value, DOWN, buff=0.5,
                                       aligned_edge=LEFT),
            FadeOut(cp_how_many)
        )

        def dis(x1, x2, y1, y2): return (x1-x2)**2 + (y1-y2)**2
        text2, number2 = value_s = VGroup(
            Text("S = ", slant=ITALIC, t2c=dict(S=YELLOW)),
            DecimalNumber(0, color=BLUE, num_decimal_places=4)
        ).arrange(RIGHT, buff=0.1).next_to(t_value, DOWN, aligned_edge=LEFT)
        f_always(number2.set_value,
                 lambda: dis(p_x(), 2, p_y(), math.sqrt(2)))
        self.wait()
        self.remove(s_value)
        self.add(value_s)
        self.play(t.animate.set_value(2), run_time=1, rate_func=linear)
        self.play(t.animate.set_value(0), run_time=2, rate_func=linear)
        self.play(t.animate.set_value(2), run_time=2, rate_func=linear)
        self.wait(3)

        t_range = Tex("(t>0)", t2c={"t": YELLOW})
        t_range.next_to(dp_square6, DOWN, aligned_edge=LEFT)
        self.play(Write(t_range))
        self.wait(3)
        self.play(FadeOut(VGroup(arrow, speed, length_cd)))


class Attention(Scene):
    def construct(self):
        def gene_label(
            label: str,
            slant: str = ITALIC,
            size: float = 36,
            color=WHITE
        ) -> Text:
            return Text(
                label, color=color, slant=slant, font_size=size
            ).set_backstroke()

        axes = Axes(x_range=(0, 2.5), y_range=(0, 6), unit_size=0.8)
        coord_a = axes.c2p(2, math.sqrt(32))
        coord_b = axes.c2p(0, 0)
        coord_c = axes.c2p(2, 0)
        coord_d = axes.c2p(2, math.sqrt(2))
        dot_b = Dot(coord_b, fill_color=BLUE_C)
        dot_a = Dot(coord_a, fill_color=BLUE_C)
        dot_c = Dot(coord_c, fill_color=BLUE_C)
        dot_d = Dot(coord_d, fill_color=BLUE_C)
        label_a = gene_label("A")
        label_b = gene_label("B")
        label_c = gene_label("C")
        label_d = gene_label("D")
        always(label_a.next_to, dot_a, UP)
        always(label_b.next_to, dot_b, DOWN)
        label_c.next_to(dot_c, DOWN)
        label_d.next_to(dot_d, RIGHT)
        triangle_abc = always_redraw(
            lambda: Polygon(dot_a.get_center(), dot_b.get_center(), coord_c
                            ).set_stroke(BLUE_C))
        rectangle = Square(0.24)
        rectangle.set_stroke(BLUE_C, width=2)
        rectangle.set_fill(BLUE_C, opacity=0.25)
        rectangle.move_to(axes.c2p(1.85, 0.15))
        segment_cd = Line(coord_c, coord_d, color=YELLOW)
        segment_cd.set_opacity(0.5)
        length_cd = Tex(r"\sqrt{2}", font_size=36)
        length_cd.next_to(segment_cd)

        dot_p = Dot(fill_color=BLUE_C)
        label_p = gene_label("P")
        dot_p.move_to(axes.c2p(1, 0))
        always(label_p.next_to, dot_p, UL, buff=0.1)
        arrow = Arrow(axes.c2p(1.6, -0.4), axes.c2p(0.4, -0.4), buff=0)
        speed = Tex(r"1\cdot s^{-1}", font_size=32).next_to(arrow, DOWN)

        t = ValueTracker(2)

        def p_on_bc():
            f_always(dot_p.move_to, lambda: axes.c2p(2 - t.get_value(), 0))

        def p_on_ab():
            f_always(dot_p.move_to, lambda: axes.c2p(
                     1 / 3 * (t.get_value() - 2),
                     math.sqrt(8 / 9) * (t.get_value() - 2)))

        p_on_bc()
        dot_e = Dot(fill_color=BLUE_C)
        dot_f = Dot(fill_color=BLUE_C)
        label_e = gene_label("E")
        label_f = gene_label("F")
        def p_x(): return axes.p2c(dot_p.get_center())[0]
        def p_y(): return axes.p2c(dot_p.get_center())[1]
        f_always(dot_e.move_to, lambda: axes.c2p(
            p_x()+p_y()-math.sqrt(2), p_y()-p_x()+2))
        f_always(dot_f.move_to, lambda: axes.c2p(
            p_y()+2-math.sqrt(2), math.sqrt(2)-p_x()+2))
        always(label_e.next_to, dot_e, UL, buff=0.1)
        always(label_f.next_to, dot_f, UL, buff=0.1)

        def dpef(): return Polygon(
            coord_d, dot_p.get_center(),
            dot_e.get_center(), dot_f.get_center()
        ).set_fill(BLUE_C, opacity=0.5).set_stroke(BLUE_C)
        square_dpef = always_redraw(dpef)

        s_label = gene_label("S", size=54, color=YELLOW)
        always(s_label.move_to, square_dpef)

        text1, number1 = t_value = VGroup(
            Text("t = ", slant=ITALIC, t2c=dict(t=YELLOW)),
            DecimalNumber(0, color=BLUE, num_decimal_places=4)
        ).arrange(RIGHT).to_corner(UL, buff=0.75)
        f_always(number1.set_value, t.get_value)

        def dis(x1, x2, y1, y2): return (x1-x2)**2 + (y1-y2)**2
        text2, number2 = s_value = VGroup(
            Text("S = ", slant=ITALIC, t2c=dict(S=YELLOW)),
            DecimalNumber(0, color=BLUE, num_decimal_places=4)
        ).arrange(RIGHT, buff=0.1).next_to(t_value, DOWN, aligned_edge=LEFT)
        f_always(number2.set_value,
                 lambda: dis(p_x(), 2, p_y(), math.sqrt(2)))

        dp_square6 = Tex("S=t^2+2", t2c={"S": YELLOW, "t": YELLOW})
        dp_square6.next_to(s_value, DOWN, buff=0.5, aligned_edge=LEFT)
        t_range = Tex("(t>0)", t2c={"t": YELLOW})
        t_range.next_to(dp_square6, DOWN, aligned_edge=LEFT)

        self.add(rectangle, label_a, label_b, label_c, label_d,
                 dot_a, dot_b, dot_c, dot_d, triangle_abc,
                 dot_p, dot_e, dot_f, label_p, label_e, label_f,
                 square_dpef, s_label, t_value, s_value,
                 dp_square6, t_range)

        t_why = VGroup(
            Tex("(0<t\\le 2)", t2c={"t": YELLOW}),
            Text("?", color=RED)
        ).arrange().next_to(t_range, DOWN, aligned_edge=LEFT)
        ex = Exmark(color=RED).move_to(t_why[1])

        whys = VGroup(
            Text("?", color=YELLOW),
            Text("?", color=YELLOW),
            Text("?", color=YELLOW))
        whys[0].move_to(Line(coord_a, coord_b))
        whys[1].move_to(Line(coord_a, coord_c))
        whys[2].move_to(Line(coord_b, coord_c))

        def rinto(x: float) -> float:
            return x ** 2

        def rfrom(x: float) -> float:
            return -1 * x ** 2 + 2 * x

        self.wait(3)
        self.play(Write(t_why))
        self.wait(3)
        self.play(t.animate.set_value(1))
        self.wait()
        self.play(t.animate.set_value(2), run_time=0.25, rate_func=rinto)
        self.play(t.animate.set_value(1), run_time=0.25, rate_func=rfrom)
        self.play(t.animate.set_value(2), run_time=0.25, rate_func=rinto)
        self.play(t.animate.set_value(1), run_time=0.25, rate_func=rfrom)
        self.wait(3)
        self.play(FadeOut(t_why))
        self.wait(3)
        self.play(
            *[FadeIn(why, scale=0.5) for why in whys],
            rate_func=there_and_back_with_pause, run_time=3)
        self.wait()
        self.play(
            dot_a.animate.move_to(axes.c2p(2, 4)),
            dot_b.animate.move_to(axes.c2p(1, 0)))
        self.wait()
        self.play(
            dot_a.animate.move_to(axes.c2p(2, 3)),
            dot_b.animate.move_to(axes.c2p(-3, 0)))
        self.wait()
        self.play(
            dot_a.animate.move_to(axes.c2p(2, 5)),
            dot_b.animate.move_to(axes.c2p(-2, 0)))
        self.wait()
        self.play(t.animate.set_value(2.5))
        self.wait(0.5)
        self.play(ShowPassingFlashAround(t_value))
        self.wait(0.5)
        self.play(
            t.animate.set_value(1),
            dot_a.animate.move_to(coord_a),
            dot_b.animate.move_to(coord_b)
        )
        self.wait()
        self.play(FadeIn(t_why))
        self.wait(0.5)
        self.play(ReplacementTransform(t_why[1], ex))
        self.wait(3)
        self.play(FadeOut(VGroup(dp_square6, t_range, t_why, ex), LEFT))


class Problem2(Scene):
    def construct(self):
        def gene_label(
            label: str,
            slant: str = ITALIC,
            size: float = 36,
            color=WHITE
        ) -> Text:
            return Text(
                label, color=color, slant=slant, font_size=size
            ).set_backstroke()

        axes = Axes(x_range=(0, 2.5), y_range=(0, 6),
                    unit_size=0.8).set_opacity(0)
        coord_a = axes.c2p(2, math.sqrt(32))
        coord_b = axes.c2p(0, 0)
        coord_c = axes.c2p(2, 0)
        coord_d = axes.c2p(2, math.sqrt(2))
        dot_a = Dot(coord_a, fill_color=BLUE_C)
        dot_b = Dot(coord_b, fill_color=BLUE_C)
        dot_c = Dot(coord_c, fill_color=BLUE_C)
        dot_d = Dot(coord_d, fill_color=BLUE_C)
        f_always(dot_a.move_to, lambda: axes.c2p(2, math.sqrt(32)))
        f_always(dot_b.move_to, lambda: axes.c2p(0, 0))
        f_always(dot_c.move_to, lambda: axes.c2p(2, 0))
        f_always(dot_d.move_to, lambda: axes.c2p(2, math.sqrt(2)))
        label_a = gene_label("A")
        label_b = gene_label("B")
        label_c = gene_label("C")
        label_d = gene_label("D")
        always(label_a.next_to, dot_a, UP)
        always(label_b.next_to, dot_b, DOWN)
        always(label_c.next_to, dot_c, DOWN)
        always(label_d.next_to, dot_d, RIGHT)
        triangle_abc = Polygon(coord_a, coord_b, coord_c)
        triangle_abc.set_stroke(BLUE_C)
        rectangle = Square(0.24)
        rectangle.set_stroke(BLUE_C, width=2)
        rectangle.set_fill(BLUE_C, opacity=0.25)
        rectangle.move_to(axes.c2p(1.85, 0.15))
        # segment_cd = Line(coord_c, coord_d, color=YELLOW)
        # segment_cd.set_opacity(0.5)
        # length_cd = Tex(r"\sqrt{2}", font_size=36)
        # length_cd.next_to(segment_cd)

        dot_p = Dot(fill_color=BLUE_C)
        label_p = gene_label("P")
        always(label_p.next_to, dot_p, UL, buff=0.1)
        # arrow = Arrow(axes.c2p(1.6, -0.4), axes.c2p(0.4, -0.4), buff=0)
        # speed = Tex(r"1\cdot s^{-1}", font_size=32).next_to(arrow, DOWN)

        t = ValueTracker(1)
        dot = Dot(fill_color=RED)
        axes2 = Axes(
            x_range=(0, 10, 2), y_range=(0, 20, 2), unit_size=0.27,
            axis_config=dict(
                include_tip=True,
                tip_config=dict(width=0.2, length=0.2)
            )
        ).shift(RIGHT*4)
        axes2_copy = axes2.copy()
        s_axe = gene_label("S").move_to(axes2.c2p(-1, 20.25))
        t_axe = gene_label("t").move_to(axes2.c2p(10.25, -1.25))
        graph_ab = axes2.get_graph(lambda x: (x - 4) ** 2 + 2,
                                   color=MAROON, x_range=[2, 8])
        graph_bc = axes2.get_graph(lambda x: x ** 2 + 2,
                                   color=PURPLE, x_range=[0, 2])

        def p_on_bc():
            f_always(dot_p.move_to, lambda: axes.c2p(2 - t.get_value(), 0))
            f_always(dot.move_to, lambda: axes2.i2gp(t.get_value(), graph_bc))

        def p_on_ab():
            f_always(dot_p.move_to, lambda: axes.c2p(
                     1 / 3 * (t.get_value() - 2),
                     math.sqrt(8 / 9) * (t.get_value() - 2)))
            f_always(dot.move_to, lambda: axes2.i2gp(t.get_value(), graph_ab))

        p_on_bc()
        dot_e = Dot(fill_color=BLUE_C)
        dot_f = Dot(fill_color=BLUE_C)
        label_e = gene_label("E")
        label_f = gene_label("F")
        def p_x(): return axes.p2c(dot_p.get_center())[0]
        def p_y(): return axes.p2c(dot_p.get_center())[1]
        f_always(dot_e.move_to, lambda: axes.c2p(
            p_x()+p_y()-math.sqrt(2), p_y()-p_x()+2))
        f_always(dot_f.move_to, lambda: axes.c2p(
            p_y()+2-math.sqrt(2), math.sqrt(2)-p_x()+2))
        always(label_e.next_to, dot_e, UL, buff=0.1)
        always(label_f.next_to, dot_f, UL, buff=0.1)

        def dpef(): return Polygon(
            dot_d.get_center(), dot_p.get_center(),
            dot_e.get_center(), dot_f.get_center()
        ).set_fill(BLUE_C, opacity=0.5).set_stroke(BLUE_C)
        square_dpef = always_redraw(dpef)

        s_label = gene_label("S", size=54, color=YELLOW)
        always(s_label.move_to, square_dpef)

        text1, number1 = t_value = VGroup(
            Text("t = ", slant=ITALIC, t2c=dict(t=YELLOW)),
            DecimalNumber(0, color=BLUE, num_decimal_places=4)
        ).arrange(RIGHT).to_corner(UL, buff=0.75)
        f_always(number1.set_value, t.get_value)

        def dis(x1, x2, y1, y2): return (x1-x2)**2 + (y1-y2)**2
        text2, number2 = s_value = VGroup(
            Text("S = ", slant=ITALIC, t2c=dict(S=YELLOW)),
            DecimalNumber(0, color=BLUE, num_decimal_places=4)
        ).arrange(RIGHT, buff=0.1).next_to(t_value, DOWN, aligned_edge=LEFT)
        f_always(number2.set_value,
                 lambda: dis(p_x(), 2, p_y(), math.sqrt(2)))

        self.add(rectangle, label_a, label_b, label_c, label_d,
                 dot_a, dot_b, dot_c, dot_d, triangle_abc,
                 dot_p, dot_e, dot_f, label_p, label_e, label_f,
                 square_dpef, s_label, t_value, s_value)
        self.wait()
        self.play(t.animate.set_value(2), rate_func=linear)
        p_on_ab()
        self.play(t.animate.set_value(8), run_time=6, rate_func=linear)
        self.wait()
        self.play(t.animate.set_value(2), run_time=0.3)
        self.wait(0.7)

        self.play(FadeIn(VGroup(axes2, t_axe, s_axe), LEFT),
                  VGroup(rectangle, triangle_abc, axes).animate.shift(LEFT*2.75))
        self.wait()
        self.play(ShowCreation(dot))
        self.wait()
        self.play(t.animate.set_value(8),
                  ShowCreation(graph_ab),
                  run_time=6, rate_func=linear)
        self.wait()

        s_6 = axes2.get_h_line(axes2.c2p(2, 6))
        s_2 = axes2.get_h_line(axes2.c2p(4, 2))
        t_4 = axes2.get_v_line(axes2.c2p(4, 2))
        s_18 = axes2.get_h_line(axes2.c2p(8, 18))
        what_relation = Tex("S = ? (t)", t2c={
            "S": YELLOW, "?": BLUE, "t": YELLOW}).to_corner(UL, buff=0.75)
        ab_how_many = Tex("AB = ?", t2c={"AB": YELLOW, "?": RED})
        ab_how_many.next_to(what_relation, DOWN, aligned_edge=LEFT)
        axe_labels = axes2.add_coordinate_labels(
            x_values=[4], y_values=[2, 6, 18], font_size=32)

        self.add(axes2_copy)
        self.play(
            FadeIn(VGroup(s_6, s_2, t_4, s_18, axe_labels), LEFT),
            FadeOut(VGroup(t_value, s_value), LEFT)
        )
        self.wait(3)
        self.play(Write(what_relation))
        self.wait()
        self.play(Write(ab_how_many))
        self.wait(5)
        self.play(FadeOut(VGroup(what_relation, ab_how_many)))
        self.play(
            Indicate(VGroup(t_4, s_2, axe_labels[0][0], axe_labels[1][0])))
        self.wait(8)
        self.play(
            Indicate(VGroup(s_6, s_18, axe_labels[1][1], axe_labels[1][2])))
        self.wait()
        self.play(t.animate.set_value(2), run_time=0.3, rate_func=rush_into)
        p_on_bc()
        self.play(t.animate.set_value(0), run_time=0.1, rate_func=rush_from)
        self.wait()
        self.play(
            t.animate.set_value(2),
            ShowCreation(graph_bc),
            run_time=2, rate_func=linear
        )
        p_on_ab()
        self.play(t.animate.set_value(8), run_time=6, rate_func=linear)
        self.wait()
        self.play(Flash(axes2.c2p(2, 6)))
        self.wait()

        relation_bc = Tex(
            "S = t ^ 2 + 2", color=PURPLE, font_size=36
        ).move_to(axes2.c2p(4.5, 7.25)).set_backstroke()
        equation = Tex(
            "t ^ 2 + 2 = 6", t2c={"t": YELLOW}
        ).next_to(what_relation, DOWN, aligned_edge=LEFT)
        solution1 = Tex(
            "t ^ 2 = 4", t2c={"t": YELLOW}
        ).next_to(equation, DOWN, aligned_edge=RIGHT)
        solution2 = Tex(
            "t = 2", t2c={"t": YELLOW}
        ).next_to(solution1, DOWN, aligned_edge=RIGHT)
        t_range = Tex(
            "(t > 0)", t2c={"t": YELLOW}
        ).next_to(solution2, DOWN, aligned_edge=RIGHT)
        axe_labels = axes2.add_coordinate_labels(
            x_values=[2, 4], y_values=[2, 6, 18], font_size=32)
        t_2 = axes2.get_v_line(axes2.c2p(2, 6))

        self.play(t.animate.set_value(2))
        self.wait()
        self.play(Flash(axe_labels[1][1], flash_radius=0.4))
        self.wait()
        self.play(Write(relation_bc))
        self.wait()
        self.play(TransformMatchingTex(
            relation_bc.copy(), equation, path_arc=PI/2,
            key_map={"t ^ 2 + 2": "t ^ 2 + 2", " = ": " = ", "S": "6"}
        ), run_time=1.5)
        self.wait(0.5)
        self.play(TransformMatchingTex(
            equation.copy(), solution1,
            key_map={"t ^ 2": "t ^ 2", " = ": " = ", "6": "4", " + 2": "4"},
        ), run_time=1)
        self.wait(0.5)
        self.play(FadeIn(t_range), rate_func=there_and_back_with_pause)
        self.wait(0.5)
        self.play(TransformMatchingTex(
            solution1.copy(), solution2,
            key_map={"t ^ 2": "t", " = ": " = ", "4": "2"}
        ), run_time=1)
        self.wait()
        self.play(ReplacementTransform(
            solution2, VGroup(t_2, axe_labels[0][0])),
            FadeOut(VGroup(equation, solution1)),
            run_time=1.25)
        self.wait()

        relation_ab = Tex(
            "S", "=", "(t-4)^2+2", t2c={"S": YELLOW, "t": YELLOW}
        ).to_corner(UL, buff=0.75)
        relation_ab2 = Tex(
            "S", "=", "(t-4)^2+2", color=MAROON, font_size=36
        ).set_backstroke().move_to(axes2.c2p(9, 19.25))
        relation_ab_eq = Tex(
            "S", "=", "a", "(t-4)^2+2",
            t2c={"S": YELLOW, "t": YELLOW, "a": BLUE}
        ).to_corner(UL, buff=0.75)
        linear_eq = Tex(
            "6=a(2-4)^2+2", t2c={"a": BLUE}
        ).next_to(relation_ab_eq, DOWN, aligned_edge=LEFT)
        linear_eq1 = Tex(
            "4a+2=6", t2c={"a": BLUE}
        ).next_to(linear_eq, DOWN, aligned_edge=LEFT)
        linear_eq2 = Tex(
            "a=1", t2c={"a": BLUE}
        ).next_to(linear_eq1, DOWN, aligned_edge=RIGHT)

        t_range2 = Tex(
            "(2\\le t\\le 8)", t2c={"t": YELLOW}
        ).next_to(relation_ab, DOWN, aligned_edge=LEFT)
        s_equation = Tex(
            "(t-4)^2+2", "=", "18", t2c={"t": YELLOW}
        ).next_to(t_range2, DOWN, aligned_edge=LEFT)
        s_solution = Tex(
            "(t-4)^2=16", t2c={"t": YELLOW}
        ).next_to(t_range2, DOWN, aligned_edge=LEFT)
        s_solution2 = Tex(
            "t-4=4", t2c={"t": YELLOW}
        ).next_to(t_range2, DOWN, aligned_edge=LEFT)
        s_solution3 = Tex(
            "t=8", t2c={"t": YELLOW}
        ).next_to(t_range2, DOWN, aligned_edge=LEFT)

        t_8 = axes2.get_v_line(axes2.c2p(8, 18))
        axe_labels = axes2.add_coordinate_labels(
            x_values=[2, 4, 8], y_values=[2, 6, 18], font_size=32)

        self.play(Flash(axes2.c2p(2, 6)), Flash(axes2.c2p(4, 2)))
        self.wait(3)
        self.play(Write(relation_ab_eq))
        self.wait()
        self.play(TransformMatchingTex(
            relation_ab_eq.copy(), linear_eq,
            key_map={"S": "6"}
        ), run_time=0.5)
        self.wait(0.25)
        self.play(TransformMatchingTex(
            linear_eq.copy(), linear_eq1, path_arc=PI/2,
            key_map={"(2-4)^2": "4"}
        ), run_time=0.5)
        self.wait(0.25)
        self.play(TransformMatchingTex(
            linear_eq1.copy(), linear_eq2,
            key_map={"6": "1", "4": "1", "+2": "1"}
        ), run_time=0.5)
        self.wait()
        self.play(
            TransformMatchingTex(relation_ab_eq, relation_ab),
            FadeOut(VGroup(linear_eq, linear_eq1, linear_eq2)),
            run_time=0.5)
        self.wait(0.5)
        self.play(TransformFromCopy(relation_ab, relation_ab2))
        self.wait()
        self.play(TransformMatchingTex(
            relation_ab.copy(), s_equation, path_arc=PI/2),
            run_time=0.75)
        self.wait(0.5)
        self.play(TransformMatchingTex(
            s_equation, s_solution,
            key_map={"+2": "16", "18": "16"}
        ), run_time=0.5)
        self.wait(0.25)
        self.play(TransformMatchingTex(
            s_solution, s_solution2,
            key_map={"(": "4", ")^2": "4", "16": "4"}
        ), run_time=0.5)
        self.wait(0.25)
        self.play(TransformMatchingTex(
            s_solution2, s_solution3,
            key_map={"4": "8"}
        ), run_time=0.5)
        self.wait()
        self.play(TransformMatchingTex(s_solution3, t_range2), run_time=1)
        self.play(ShowCreation(t_8))
        self.play(Write(axe_labels[0][2]))
        self.wait(5)

        segment_cb = Line(dot_c.get_center(), dot_b.get_center())
        segment_ba = Line(dot_b.get_center(), dot_a.get_center())
        elbow_cba = VGroup(segment_cb, segment_ba).set_color(YELLOW)
        bc_value = Tex(
            "BC=2", t2c={"BC": YELLOW}
        ).to_edge(UP, buff=0.75)
        abc_value = Tex(
            "AB+BC=8", t2c={"AB": YELLOW, "BC": YELLOW}
        ).next_to(bc_value, DOWN)
        bc_value.align_to(abc_value, LEFT)
        ab_equation = Tex(
            "AB=8-2", t2c={"AB": YELLOW}
        ).next_to(abc_value, DOWN, aligned_edge=LEFT)
        ab_value = Tex(
            "AB=6", t2c={"AB": YELLOW}
        ).next_to(abc_value, DOWN).align_to(ab_equation, LEFT)

        self.play(ShowCreationThenDestruction(segment_cb))
        self.play(Indicate(VGroup(t_2, axe_labels[0][0])))
        self.wait()
        self.play(Write(bc_value))
        self.wait()
        self.play(ShowCreationThenDestruction(elbow_cba))
        self.play(Indicate(VGroup(t_8, axe_labels[0][2])))
        self.wait()
        self.play(Write(abc_value))
        self.wait()
        self.play(TransformMatchingTex(
            abc_value.copy(), ab_equation,
            key_map={"+": "-", "BC": "2"}
        ), run_time=0.75)
        self.wait(0.5)
        self.play(TransformMatchingTex(
            ab_equation, ab_value, key_map={"8-2": "6"}
        ), run_time=0.75)
        self.wait()
        self.play(ab_value.animate.next_to(t_range2, DOWN, aligned_edge=LEFT))
        self.play(FadeOut(VGroup(abc_value, bc_value)))
        self.wait(7)
        self.play(FadeOut(VGroup(
            relation_ab, t_range2, ab_value, rectangle,
            label_a, label_b, label_c, label_d,
            dot_a, dot_b, dot_c, dot_d, triangle_abc,
            dot_p, dot_e, dot_f, label_p, label_e, label_f,
            square_dpef, s_label
        ), LEFT), VGroup(
            axes2_copy, graph_ab, graph_bc, relation_ab2,
            relation_bc, t_2, t_4, t_8, s_2, s_6, s_18,
            axe_labels, axes2, t_axe, s_axe
        ).animate.move_to(RIGHT*0.25), run_time=2)
        self.play(FadeOut(dot))


class Problem3(Scene):
    def construct(self):
        s = ValueTracker(3)
        axes = Axes(
            x_range=(0, 10, 2), y_range=(0, 20, 2), unit_size=0.27,
            axis_config=dict(
                include_tip=True,
                tip_config=dict(width=0.2, length=0.2))
        ).move_to(UP*0.17 + RIGHT*0.12)
        axes.add_coordinate_labels([2, 4, 8], [2, 6, 18], font_size=32)
        t_2 = axes.get_v_line(axes.c2p(2, 6))
        t_4 = axes.get_v_line(axes.c2p(4, 2))
        t_8 = axes.get_v_line(axes.c2p(8, 18))
        s_2 = axes.get_h_line(axes.c2p(4, 2))
        s_6 = axes.get_h_line(axes.c2p(2, 6))
        s_18 = axes.get_h_line(axes.c2p(8, 18))
        t_axe = Text("t", font_size=36, slant=ITALIC)
        t_axe.move_to(axes.c2p(10.25, -1.25))
        s_axe = Text("S", font_size=36, slant=ITALIC)
        s_axe.move_to(axes.c2p(-1, 20.25))
        graph_bc = axes.get_graph(lambda x: x ** 2 + 2,
                                  color=PURPLE, x_range=(0, 2))
        graph_ab = axes.get_graph(lambda x: (x - 4) ** 2 + 2,
                                  color=MAROON, x_range=(2, 8))
        label_bc = Tex("S=t^2+2", font_size=36, color=PURPLE)
        label_bc.move_to(axes.c2p(4.5, 7.25))
        label_ab = Tex("S", "=", "(t-4)^2+2", font_size=36, color=MAROON)
        label_ab.move_to(axes.c2p(9, 19.25))

        self.add(VGroup(axes, t_2, t_4, t_8, s_2, s_6, s_18, t_axe, s_axe,
                        graph_bc, graph_ab, label_bc, label_ab))

        v_line1 = axes.get_v_line(axes.c2p(1, 3))
        v_line2 = axes.get_v_line(axes.c2p(3, 3))
        v_line3 = axes.get_v_line(axes.c2p(5, 3))
        t1_label = Tex("t_1", font_size=32, color=YELLOW)
        t1_label.next_to(v_line1, DOWN, buff=0.5)
        t2_label = Tex("t_2", font_size=32, color=YELLOW)
        t2_label.next_to(v_line2, DOWN, buff=0.5)
        t3_label = Tex("t_3", font_size=32, color=YELLOW)
        t3_label.next_to(v_line3, DOWN, buff=0.5)
        h_line1 = axes.get_h_line(axes.c2p(1, 3))
        h_line2 = axes.get_h_line(axes.c2p(3, 3))
        h_line3 = axes.get_h_line(axes.c2p(5, 3))
        s_label = Tex("S", font_size=32, color=YELLOW)
        s_label.next_to(h_line1, LEFT, buff=0.5)
        v_lines = VGroup(v_line1, v_line2, v_line3)
        h_lines = VGroup(h_line1, h_line2, h_line3)
        t_labels = VGroup(t1_label, t2_label, t3_label)
        t1_plus_t2 = Tex(
            "t_1+t_2=?", t2c={"t_1": YELLOW, "t_2": YELLOW, "?": RED}
        ).to_corner(UL, buff=0.75)
        when = VGroup(
            TexText("When"),
            Tex("t_3=4 t_1,", t2c={"t_1": YELLOW, "t_3": YELLOW, "4": BLUE})
        ).arrange().next_to(t1_plus_t2, DOWN, aligned_edge=LEFT)
        s_how_many = Tex(
            "S=?", t2c={"S": YELLOW, "?": RED}
        ).next_to(when, DOWN, aligned_edge=LEFT)

        self.wait(3)
        self.play(*[Write(t) for t in t_labels])
        self.wait()
        self.play(*[ShowCreation(v) for v in v_lines])
        self.play(*[ShowCreation(h) for h in h_lines])
        self.wait(0.5)
        self.play(Write(s_label))
        self.wait()
        self.play(Write(t1_plus_t2))
        self.wait()
        self.play(Write(when))
        self.wait(0.5)
        self.play(Write(s_how_many))
        self.wait(3)
        self.play(FadeOut(VGroup(t1_plus_t2, when, s_how_many)))
        self.play(FadeOut(VGroup(
            s_label, t1_label, t2_label, t3_label, h_line1, h_line2,
            h_line3, v_line1, v_line2, v_line3)))
        self.wait(5)

        y_equals_s = axes.get_graph(lambda x: s.get_value(), color=BLUE)
        y_eq_s = always_redraw(
            lambda: axes.get_graph(lambda x: s.get_value(), color=BLUE))
        text, num = y_eq_s_label = VGroup(
            Text("S=", color=BLUE, slant=ITALIC),
            DecimalNumber(color=BLUE, num_decimal_places=3)
        )
        y_eq_s_label.arrange(RIGHT)
        f_always(num.set_value, s.get_value)
        y_eq_s_label.move_to(axes.c2p(16, 6))

        def calc_t3(s: float) -> float:
            if s < 2:
                return -100
            return 4 + math.sqrt(s - 2)

        def calc_t1(s: float) -> float:
            if s < 2 or s > 6:
                return -100
            return math.sqrt(s - 2)

        dot_t1 = Dot(fill_color=BLUE)
        dot_t2 = Dot(fill_color=BLUE)
        dot_t3 = Dot(fill_color=BLUE)
        f_always(dot_t1.move_to,
                 lambda: axes.c2p(calc_t1(s.get_value()), s.get_value()))
        f_always(dot_t2.move_to,
                 lambda: axes.c2p(4 - calc_t1(s.get_value()), s.get_value()))
        f_always(dot_t3.move_to,
                 lambda: axes.c2p(calc_t3(s.get_value()), s.get_value()))
        v_line_1 = always_redraw(lambda: axes.get_v_line(dot_t1.get_bottom()))
        v_line_2 = always_redraw(lambda: axes.get_v_line(dot_t2.get_bottom()))
        v_line_3 = always_redraw(lambda: axes.get_v_line(dot_t3.get_bottom()))
        always(t1_label.next_to, v_line_1, DOWN, buff=0.5)
        always(t2_label.next_to, v_line_2, DOWN, buff=0.5)
        always(t3_label.next_to, v_line_3, DOWN, buff=0.5)

        self.play(ShowCreation(y_equals_s))
        self.play(Write(y_eq_s_label))
        self.wait()
        self.play(Write(dot_t1), Write(dot_t2), Write(dot_t3))
        self.wait(0.5)
        self.play(
            ShowCreation(v_line_1), Write(t1_label),
            ShowCreation(v_line_2), Write(t2_label),
            ShowCreation(v_line_3), Write(t3_label),
        )
        self.wait()
        self.remove(y_equals_s)
        self.add(y_eq_s)
        self.play(s.animate.set_value(0))
        self.wait()
        self.play(s.animate.set_value(10), run_time=10, rate_func=linear)
        self.wait(3)
        self.play(s.animate.set_value(3))
        self.wait(5)

        t1_eq = Tex(
            "t_1^2+2=S", t2c={"t_1": YELLOW, "S": BLUE}
        ).to_corner(UL, buff=0.75)
        t1_sq = Tex(
            "t_1^2=S-2", t2c={"t_1": YELLOW, "S": BLUE}
        ).to_corner(UL, buff=0.75)
        t1_value = Tex(
            "t_1=\\sqrt{S-2}", t2c={"t_1": YELLOW, "S": BLUE}
        ).to_corner(UL, buff=0.75)

        t2_eq = Tex(
            "(t_2-4)^2+2=S", t2c={"t_2": YELLOW, "S": BLUE}
        ).next_to(t1_eq, DOWN, aligned_edge=LEFT)
        t2_sq = Tex(
            "(t_2-4)^2=S-2", t2c={"t_2": YELLOW, "S": BLUE}
        ).next_to(t1_eq, DOWN, aligned_edge=LEFT)
        t2_sq2 = Tex(
            "t_2-4=-\\sqrt{S-2}", t2c={"t_2": YELLOW, "S": BLUE}
        ).next_to(t1_eq, DOWN, aligned_edge=LEFT)
        t2_value = Tex(
            "t_2=4-\\sqrt{S-2}", t2c={"t_2": YELLOW, "S": BLUE}
        ).next_to(t1_eq, DOWN, aligned_edge=LEFT)

        t3_eq = Tex(
            "(t_3-4)^2+2=S", t2c={"t_3": YELLOW, "S": BLUE}
        ).next_to(t2_eq, DOWN, aligned_edge=LEFT)
        t3_sq = Tex(
            "(t_3-4)^2=S-2", t2c={"t_3": YELLOW, "S": BLUE}
        ).next_to(t2_eq, DOWN, aligned_edge=LEFT)
        t3_sq2 = Tex(
            "t_3-4=\\sqrt{S-2}", t2c={"t_3": YELLOW, "S": BLUE}
        ).next_to(t2_eq, DOWN, aligned_edge=LEFT)
        t3_value = Tex(
            "t_3=4+\\sqrt{S-2}", t2c={"t_3": YELLOW, "S": BLUE}
        ).next_to(t2_eq, DOWN, aligned_edge=LEFT)

        t_relation = Tex(
            "(0<t_1<t_2<t_3)",
            t2c={"t_1": YELLOW, "t_2": YELLOW, "t_3": YELLOW}
        ).next_to(t3_eq, DOWN, aligned_edge=LEFT)

        self.play(Write(t1_eq), Write(t2_eq), Write(t3_eq))
        self.wait()
        self.play(
            TransformMatchingTex(t1_eq, t1_sq),
            TransformMatchingTex(t2_eq, t2_sq),
            TransformMatchingTex(t3_eq, t3_sq),
            run_time=0.5
        )
        self.wait(0.5)
        self.play(FadeIn(t_relation), run_time=1,
                  rate_func=there_and_back_with_pause)
        self.wait(0.5)
        self.play(
            TransformMatchingTex(t1_sq, t1_value, key_map={"^2": "\\sqrt"}),
            TransformMatchingTex(t2_sq, t2_sq2, key_map={"^2": "\\sqrt"}),
            TransformMatchingTex(t3_sq, t3_sq2, key_map={"^2": "\\sqrt"}),
            run_time=0.5
        )
        self.wait(0.5)
        self.play(
            TransformMatchingTex(t2_sq2, t2_value),
            TransformMatchingTex(t3_sq2, t3_value),
            run_time=0.75
        )
        self.wait(3)

        t1_add_t2_value = Tex(
            "t_1+t_2=4", t2c={"t_1": YELLOW, "t_2": YELLOW}
        ).next_to(t3_eq, DOWN, aligned_edge=LEFT)
        s_value = Tex(
            "S=\\frac{34}{9}", t2c={"S": BLUE}
        ).next_to(t1_add_t2_value, DOWN, aligned_edge=LEFT)
        t1_add_t2 = Tex(
            """
            &t_1+t_2 \\\\
            =&\\sqrt{S-2}+4-\\sqrt{S-2} \\\\
            =&4
            """,
            t2c={"t_1": YELLOW, "t_2": YELLOW, "S": BLUE}
        ).next_to(t1_add_t2_value, DOWN, aligned_edge=LEFT)
        # s_eq = Tex(
        #     """
        #     t_3&=4t_1 \\\\
        #     4+\\sqrt{S-2}&=4\\sqrt{S-2} \\\\
        #     4&=3\\sqrt{S-2} \\\\
        #     \\sqrt{S-2}&=\\frac{4}{3} \\\\
        #     S-2&=\\frac{16}{9} \\\\
        #     S&=\\frac{34}{9}
        #     """,
        #     t2c={"t_1": YELLOW, "t_3": YELLOW, "S": BLUE}
        # ).next_to(t1_add_t2_value, DOWN, aligned_edge=LEFT)
        s_eq = Tex(
            """
            t_3&=4t_1 \\\\
            4+\\sqrt{S-2}&=4\\sqrt{S-2} \\\\
            4&=3\\sqrt{S-2} \\\\
            \\sqrt{S-2}&=\\frac{4}{3}
            """,
            t2c={"t_1": YELLOW, "t_3": YELLOW, "S": BLUE}
        ).next_to(t1_add_t2_value, DOWN, aligned_edge=LEFT)
        s_eq2 = Tex(
            """
            \\sqrt{S-2}&=\\frac{4}{3}
            """,
            t2c={"S": BLUE}
        ).next_to(t1_add_t2_value, DOWN, aligned_edge=LEFT)
        s_eq3 = Tex(
            """
            \\sqrt{S-2}&=\\frac{4}{3} \\\\
            S-2&=\\frac{16}{9} \\\\
            S&=\\frac{34}{9}
            """,
            t2c={"S": BLUE}
        ).next_to(t1_add_t2_value, DOWN, aligned_edge=LEFT)

        self.play(Write(t1_add_t2), run_time=1.5)
        self.wait(3)
        self.play(TransformMatchingTex(t1_add_t2, t1_add_t2_value),
                  run_time=1)
        self.wait()
        self.play(Write(s_eq), run_time=2)
        self.wait(0.5)
        self.play(TransformMatchingTex(s_eq, s_eq2), run_time=1)
        self.wait(0.5)
        self.bring_to_front(s_eq2)
        self.play(Write(s_eq3))
        self.remove(s_eq2)
        self.wait()
        self.play(TransformMatchingTex(s_eq3, s_value), run_time=1)
        self.wait(10)

        symmetry = axes.get_v_line(axes.c2p(2, 20)).set_color(YELLOW)
        symmetry2 = axes.get_v_line(axes.c2p(4, 20)).set_color(YELLOW)
        graph_bc_copy = graph_bc.copy().set_color(YELLOW)

        self.play(ShowCreation(symmetry), ShowCreation(symmetry2), run_time=1)
        self.wait()
        self.play(ShowCreation(graph_bc_copy))
        self.wait()
        self.play(graph_bc_copy.animate.flip(UP, about_point=axes.c2p(2, 4)))
        self.wait()
        self.play(graph_bc_copy.animate.flip(UP, about_point=axes.c2p(4, 4)))
        self.wait(3)
        self.play(FadeOut(VGroup(graph_bc_copy, symmetry, symmetry2)))
        self.wait(15)
        self.play(*[FadeOut(mob) for mob in self.get_mobjects()])


class Congratulations(Scene):
    def construct(self):
        congratulations = Text(
            'Congratulations!', font_size=128, color="#ff3232")
        self.play(Write(congratulations))
        now = self.time

        def updater(mob: VMobject) -> VMobject:
            hsv = [(self.time - now) % 1, 0.8, 1]
            rgb = colorsys.hsv_to_rgb(*hsv)
            rgb = np.array(list(rgb))
            return mob.set_color(rgb_to_color(rgb))
        congratulations.add_updater(updater)
        self.wait(20)
