from manim import *
import random


def create_textbox(text, sz=1, indx=None, show_index=False, color=WHITE):
    box = Rectangle(width=sz, height=sz, color=color)
    text = Text(text, font_size=DEFAULT_FONT_SIZE * sz)
    text.move_to(box.get_center())
    grp = VGroup(box, text)
    if show_index:
        indx = Text(
            str(indx), font_size=DEFAULT_FONT_SIZE * sz * 0.65, weight=THIN
        ).next_to(box, DOWN * sz)
        grp.add(indx)
    return grp


def create_array(numbers, show_index=False, sz=1, color=WHITE):
    textboxes = [
        create_textbox(num, sz, i, show_index=show_index, color=color)
        for i, num in enumerate(numbers)
    ]
    group = VGroup(*textboxes)
    group.arrange(RIGHT)
    return group


class Introduction(Scene):
    def l(self, *args):
        return MathTex(*args, font_size=DEFAULT_FONT_SIZE * 0.8).next_to(
            self.array1, DOWN * 2.5
        )

    def do_example(self, i, j):
        t0 = self.l(f"m({i}, {j}) =")
        self.play(FadeIn(t0))
        t1 = self.l(
            f"m({i}, {j}) =", r"\text{min of index }", f"{i}", r"\text{ to }", f"{j}"
        )
        t2 = self.l(
            f"m({i}, {j}) =",
            f"min({', '.join([str(num) for num in self.nums[i:j+1]])})",
        )
        t3 = self.l(f"m({i}, {j}) =", f"{min(self.nums[i:j+1])}")
        self.play(Transform(t0, t1))
        self.wait(1)
        anims = []
        for k in range(i, j + 1):
            anims.append(self.array1[k].animate.set_color(YELLOW))
        self.play(AnimationGroup(*anims, lag_ratio=0.5, run_time=1.5))
        self.wait(1)
        self.play(Transform(t0, t2))
        self.wait(1)
        self.play(Transform(t0, t3))
        self.play(
            Indicate(
                self.array1[self.nums.index(min(self.nums[i : j + 1]), i)], color=YELLOW
            )
        )
        anims = []
        for k in range(i, j + 1):
            anims.append(self.array1[k].animate.set_color(WHITE))
        self.play(AnimationGroup(*anims), FadeOut(t0))

    def construct(self):
        title = Text("Range Minimum Query", font_size=DEFAULT_FONT_SIZE * 1.5).shift(
            UP * 2.6
        )
        N = 12
        self.nums = [7, 4, 5, 8, 1, 5, 7, 1, 8, 8, 6, 5]
        print(self.nums)
        self.array1 = create_array(map(str, self.nums), show_index=True, sz=0.8).shift(
            UP * 0
        )
        self.add(title)
        self.play(Create(self.array1))

        t1 = self.l(f"m(L, R) =", r"\text{min of index }", f"L", r"\text{ to }", f"R")
        self.play(Write(t1))
        self.wait(1)
        self.play(FadeOut(t1))

        self.do_example(3, 5)
        self.do_example(0, 4)

        trivial = self.l(r"\text{Trivial Solution: } \mathcal{O}(N) \text{ per query}")
        self.play(Create(trivial))
        self.wait(0.5)
        self.play(FadeOut(trivial))


def create_grid(n, sz):
    box = Rectangle(
        width=sz * n, height=sz * n, grid_xstep=(sz * n) / n, grid_ystep=(sz * n) / n
    )
    left_label = []
    top_label = []
    for i in range(0, n):
        coord = box.get_left() + box.get_top() + LEFT * sz * 0.5
        coord += DOWN * (i * sz + sz / 2)
        left_label.append(
            Text(str(i), font_size=DEFAULT_FONT_SIZE * sz * 0.65).move_to(coord)
        )
    for i in range(0, n):
        coord = box.get_left() + box.get_top() + UP * sz * 0.5
        coord += RIGHT * (i * sz + sz / 2)
        top_label.append(
            Text(str(i), font_size=DEFAULT_FONT_SIZE * sz * 0.65).move_to(coord)
        )
    return VGroup(box, *left_label, *top_label)


class NSquared(Scene):
    def construct(self):
        N = 5
        sz = 0.8 * 1.33
        self.nums = [7, 2, 3, 1, 5]
        self.array = create_array(
            map(str, self.nums), show_index=False, sz=sz / 1.33
        ).shift(UP * 3)
        self.grid = create_grid(N, sz).next_to(self.array, DOWN).shift(LEFT * 0.35)
        self.play(FadeIn(self.array))
        self.wait(0.5)
        self.play(FadeIn(self.grid))

        t0 = []
        t1 = []
        for i in range(N):
            for j in range(N):
                if j < i:
                    continue
                coord = (
                    self.grid[0].get_left()
                    + self.grid[0].get_top()
                    + RIGHT * sz * 0.5
                    + UP * sz * 0.5
                )
                coord += RIGHT * j * sz
                coord += DOWN * i * sz
                t0.append(
                    Text(
                        f"m({i},{j})", font_size=DEFAULT_FONT_SIZE * 0.5, color=YELLOW
                    ).move_to(coord)
                )
                t1.append(
                    Text(
                        str(min(self.nums[i : j + 1])),
                        font_size=DEFAULT_FONT_SIZE * sz,
                        color=YELLOW,
                    ).move_to(coord)
                )
        # self.add((VGroup(*t0)))
        m = VGroup(*t0[:N])
        m1 = VGroup(*t1[:N])
        self.play(Create(m))
        self.wait(0.4)
        self.play(Transform(m, m1))
        self.wait(0.4)
        self.play(FadeIn(*t1[N:]))

        self.play(
            m.animate.shift(LEFT * 3),
            self.array.animate.shift(LEFT * 3),
            self.grid.animate.shift(LEFT * 3),
            *(x.animate.shift(LEFT * 3) for x in t1[N:]),
        )
        font_size = DEFAULT_FONT_SIZE
        pre_mem = MathTex(
            r"\text{Preprocessing: }", r"\mathcal{O}(N^2)", font_size=font_size
        ).shift(UP + RIGHT * 3)
        query_time = MathTex(
            r"\text{Query: }", r"\mathcal{O}(1)", font_size=font_size
        ).next_to(pre_mem, DOWN * 2)
        query_time[0].align_to(pre_mem[0], RIGHT)
        query_time[1].align_to(pre_mem[1], LEFT)

        self.play(Write(pre_mem))
        self.play(Write(query_time))
        # self.play(FadeOut(pre_mem, pre_time, query_time))


c_col = YELLOW
left_col = RED
right_col = BLUE
N = 16
sz = 0.5


class Fast(Scene):
    def construct(self):
        # self.nums = [random.randint(1, 9) for i in range(N)]
        self.nums = [6, 3, 1, 6, 2, 8, 5, 7, 9, 6, 7, 8, 9, 4, 7, 3]
        self.a3()

    def a1(self):
        self.array = create_array(map(str, self.nums), show_index=True, sz=sz).shift(
            UP * 2
        )

        self.add(self.array)
        self.a = create_array([""] * N, sz=sz).next_to(self.array, DOWN)
        self.a_label = MathTex("A_1").next_to(self.a, LEFT)

        self.ex1 = MathTex("m(3, 14)")
        self.ex2 = MathTex(
            "m(3, 14)", "=", "min(", "m(3, 7)", ",", "m(8, 14)", ")"
        ).move_to(self.ex1)
        self.ex2[3].set_color(left_col)
        self.ex2[5].set_color(right_col)
        self.wait(0.5)
        self.play(Write(self.ex1))
        anims = []
        for k in range(3, 15):
            anims.append(self.array[k].animate.set_color(GREEN))
        self.play(AnimationGroup(*anims, run_time=1.5))

        line = DashedLine(
            self.array.get_center() + UP * sz,
            self.a.get_center() + DOWN * sz,
            color=c_col,
        )
        self.wait(0.4)
        self.play(Create(line))
        self.wait(0.4)
        anims = []
        for k in range(3, 15):
            anims.append(
                self.array[k].animate.set_color(left_col if k < 8 else right_col)
            )
        self.play(AnimationGroup(*anims, run_time=1.5))
        self.wait(0.5)
        self.play(Transform(self.ex1, self.ex2))
        anims = []
        for k in range(3, 15):
            anims.append(self.array[k].animate.set_color(WHITE))
        self.play(AnimationGroup(*anims, run_time=1.5), FadeOut(self.ex1))
        self.wait(0.5)
        self.play(FadeIn(self.a), FadeIn(self.a_label))

        self.a_txts = [None] * N

        for k in range(N // 2 - 1, -1, -1):
            # for k in [N//2 -1]:
            anims = []
            anims.append(self.a[k].animate.set_color(left_col))
            for l in range(k, N // 2):
                anims.append(self.array[l].animate.set_color(left_col))
            formula = MathTex(
                f"A_1[",
                f"{k}",
                f"]= m(",
                f"{k}",
                ",",
                f"{N//2-1})",
                font_size=DEFAULT_FONT_SIZE * sz * 1.5,
            ).next_to(self.a[k], DOWN * 4)
            formula[1].set_color(left_col)
            formula[3].set_color(left_col)
            formula[5].set_color(c_col)
            anims.append(FadeIn(formula))
            self.play(AnimationGroup(*anims, run_time=0.5))
            val = min(self.nums[k : N // 2])
            self.a_txts[k] = Text(str(val), font_size=DEFAULT_FONT_SIZE * sz).move_to(
                self.a[k][1].get_center() + self.a[k].get_center()
            )
            self.play(Write(self.a_txts[k]))

            anims = []
            anims.append(self.a[k].animate.set_color(WHITE))
            # for l in range(k, N // 2):
            #     anims.append(self.array[l].animate.set_color(WHITE))
            anims.append(FadeOut(formula))
            self.play(AnimationGroup(*anims, run_time=0.2))
            self.wait(0.5)

        anims = []
        for l in range(k, N // 2):
            anims.append(self.array[l].animate.set_color(WHITE))
        self.play(AnimationGroup(*anims, run_time=0.2))

        for k in range(N // 2, N):
            # for k in [N//2 -1]:
            anims = []
            anims.append(self.a[k].animate.set_color(right_col))
            for l in range(N // 2, k + 1):
                anims.append(self.array[l].animate.set_color(right_col))

            formula = MathTex(
                f"A_1[",
                f"{k}",
                f"]= m(",
                f"{N//2}",
                ",",
                f"{k})",
                font_size=DEFAULT_FONT_SIZE * sz * 1.5,
            ).next_to(self.a[k], DOWN * 4)
            formula[1].set_color(right_col)
            formula[3].set_color(c_col)
            formula[5].set_color(right_col)
            anims.append(FadeIn(formula))

            self.play(AnimationGroup(*anims, run_time=0.5))
            val = min(self.nums[N // 2 : k + 1])
            self.a_txts[k] = Text(str(val), font_size=DEFAULT_FONT_SIZE * sz).move_to(
                self.a[k][1].get_center() + self.a[k].get_center()
            )
            self.play(Write(self.a_txts[k]))

            # self.wait(0.3)
            anims = []
            anims.append(self.a[k].animate.set_color(WHITE))
            # for l in range(N // 2, k + 1):
            #     anims.append(self.array[l].animate.set_color(WHITE))
            anims.append(FadeOut(formula))
            self.play(AnimationGroup(*anims, run_time=0.2))
            self.wait(0.5)

        anims = []
        for l in range(N // 2, k + 1):
            anims.append(self.array[l].animate.set_color(WHITE))
        self.play(AnimationGroup(*anims, run_time=0.2))

        i = 3
        j = 14
        c = N // 2
        self.q1 = MathTex("m(3, 14)").shift(DOWN)
        self.q2 = MathTex(
            "m(3, 14)", "=", "min(", "m(3, 7)", ",", "m(8, 14)", ")"
        ).move_to(self.q1)
        self.q2[3].set_color(left_col)
        self.q2[5].set_color(right_col)
        self.q3 = MathTex(
            "m(3, 14)", "=", "min(", "A_1[3]", ",", "A_1[14]", ")"
        ).move_to(self.q1)
        self.q3[3].set_color(left_col)
        self.q3[5].set_color(right_col)

        self.play(Write(self.q1))
        anims = []
        for k in range(i, j + 1):
            anims.append(self.array[k].animate.set_color(GREEN))
        self.play(AnimationGroup(*anims, run_time=1.5))

        anims = []
        for k in range(i, j + 1):
            anims.append(
                self.array[k].animate.set_color(left_col if k < c else right_col)
            )
        self.play(Transform(self.q1, self.q2), AnimationGroup(*anims, run_time=1.5))

        anims = []
        anims.append(self.a[i].animate.set_color(left_col))
        anims.append(self.a[j].animate.set_color(right_col))
        anims.append(self.a_txts[i].animate.set_color(left_col))
        anims.append(self.a_txts[j].animate.set_color(right_col))
        self.play(Transform(self.q1, self.q3), AnimationGroup(*anims, run_time=1.5))
        indi = lambda x: Wiggle(x, scale_value=1.5)
        self.play(indi(self.a[i]), indi(self.a_txts[i]))
        self.play(indi(self.a[j]), indi(self.a_txts[j]))
        self.play(FadeOut(self.q1))

        # NOW SHOW THE EQUATION
        self.txt_ij = MathTex(
            "L", r"<", "8", r"\leq", "R", font_size=DEFAULT_FONT_SIZE
        ).shift(DOWN)
        self.txt_ij.set_color_by_tex("8", c_col)
        self.txt_ij.set_color_by_tex("L", left_col)
        self.txt_ij.set_color_by_tex("R", right_col)
        self.play(Write(self.txt_ij))

        self.q1 = MathTex("m(", "L", ",", "R", ")").next_to(self.txt_ij, DOWN)
        self.q1[1].set_color(left_col)
        self.q1[3].set_color(right_col)
        self.play(Write(self.q1))
        self.q2 = MathTex(
            "m(", "L", ",", "R", ")", "=", "min(", "m(L, 7)", ",", "m(8, R)", ")"
        ).move_to(self.q1)
        self.q2[1].set_color(left_col)
        self.q2[7].set_color(left_col)
        self.q2[3].set_color(right_col)
        self.q2[9].set_color(right_col)
        self.q3 = MathTex(
            "m(", "L", ",", "R", ")", "=", "min(", "A_1[L]", ",", "A_1[R]", ")"
        ).move_to(self.q1)
        self.q3[1].set_color(left_col)
        self.q3[7].set_color(left_col)
        self.q3[3].set_color(right_col)
        self.q3[9].set_color(right_col)

        self.wait(0.5)
        self.play(Transform(self.q1, self.q2))
        self.wait(0.5)
        self.play(Transform(self.q1, self.q3))
        anims = []
        for k in range(i, j + 1):
            anims.append(self.array[k].animate.set_color(WHITE))
        self.play(
            FadeOut(self.q1, self.a, *self.a_txts, line, self.txt_ij, self.a_label),
            AnimationGroup(*anims),
        )

    def a2(self):
        self.array = create_array(map(str, self.nums), show_index=True, sz=sz).shift(
            UP * 2
        )

        def get_x_between(l):
            return (
                self.array[l].get_center()[0] + self.array[l + 1].get_center()[0]
            ) / 2

        dashed_line_x = [get_x_between(N // 4 - 1), get_x_between(3 * (N // 4) - 1)]
        solid_line_x = [0]
        self.add(self.array)

        self.a = create_array([""] * N, sz=sz).next_to(self.array, DOWN)
        self.a_label = MathTex("A_2").next_to(self.a, LEFT)

        top = UP * 2 * sz
        bottom = DOWN * sz

        solid_lines = []
        for x in solid_line_x:
            solid_lines.append(
                Line(
                    self.array.get_center() + top + RIGHT * x,
                    self.a.get_center() + bottom + RIGHT * x,
                    color=c_col,
                )
            )
        self.play(Create(*solid_lines))
        self.wait(0.5)

        dashed_lines = []
        for x in dashed_line_x:
            dashed_lines.append(
                DashedLine(
                    self.array.get_center() + top + RIGHT * x,
                    self.a.get_center() + bottom + RIGHT * x,
                    color=c_col,
                )
            )

        self.play(FadeIn(*dashed_lines))
        self.wait(0.5)
        self.play(FadeIn(self.a, self.a_label))

        self.a_txts = [None] * N

        def color_range(k, mid, col, going_right):
            ll = min(k, mid)
            rr = max(k, mid)
            anims = []
            anims.append(self.a[k].animate.set_color(col))
            for l in range(ll, rr + 1):
                anims.append(self.array[l].animate.set_color(col))
            formula = MathTex(
                f"A_2[",
                f"{k}",
                f"]= m(",
                f"{ll}",
                ",",
                f"{rr})",
                font_size=DEFAULT_FONT_SIZE * sz * 1.5,
            ).next_to(self.a[k], DOWN * 4)
            formula[1].set_color(col)
            formula[3].set_color(c_col if going_right else col)
            formula[5].set_color(col if going_right else c_col)
            anims.append(FadeIn(formula))
            up_factor = UP * 1.5 * sz
            if not going_right:
                arrow = Arrow(
                    start=self.array[mid].get_center() + up_factor + RIGHT * sz,
                    end=self.array[k].get_center() + LEFT * sz * 0.8 + up_factor,
                    color=col,
                    max_tip_length_to_length_ratio=1000,
                    max_stroke_width_to_length_ratio=1000,
                    tip_length=0.25,
                    tip_shape=ArrowSquareTip,
                )
            else:
                arrow = Arrow(
                    start=self.array[mid].get_center() + up_factor + LEFT * sz,
                    end=self.array[k].get_center() + RIGHT * sz * 0.8 + up_factor,
                    color=col,
                    max_tip_length_to_length_ratio=1000,
                    max_stroke_width_to_length_ratio=1000,
                    tip_length=0.25,
                    tip_shape=ArrowSquareTip,
                )
            if k == mid:
                arrow = None
            elif abs(k - mid) == 1:
                anims.append(Create(arrow))
                self.og_arrow = arrow
            else:
                anims.append(Transform(self.og_arrow, arrow))
            self.play(AnimationGroup(*anims, run_time=0.5))
            val = min(self.nums[ll : rr + 1])
            self.a_txts[k] = Text(
                str(val), font_size=DEFAULT_FONT_SIZE * sz, color=col
            ).move_to(self.a[k][1].get_center() + self.a[k].get_center())
            self.play(Create(self.a_txts[k]))

            anims = []
            anims.append(self.a[k].animate.set_color(WHITE))
            anims.append(self.a_txts[k].animate.set_color(WHITE))
            # for l in range(ll, rr + 1):
            #     anims.append(self.array[l].animate.set_color(WHITE))
            anims.append(FadeOut(formula))
            self.play(AnimationGroup(*anims, run_time=0.2))
            self.wait(0.5)

        lols = []    
        for k in range(N // 4 - 1, -1, -1):
            color_range(k, N // 4 - 1, left_col, going_right=False)
        for k in range(N // 4 - 1, -1, -1):
            lols.append(self.array[k].animate.set_color(WHITE))
        self.play(AnimationGroup(*lols, run_time=0.2))

        lols = []
        for k in range(N // 4, N // 2):
            color_range(k, N // 4, right_col, going_right=True)
        for k in range(N // 4, N // 2):
            lols.append(self.array[k].animate.set_color(WHITE))
        self.play(AnimationGroup(*lols, run_time=0.2))


        lols = []
        for k in range(3 * (N // 4) - 1, N // 2 - 1, -1):
            color_range(k, 3 * (N // 4) - 1, left_col, going_right=False)
        for k in range(3 * (N // 4) - 1, N // 2 - 1, -1):
            lols.append(self.array[k].animate.set_color(WHITE))
        self.play(AnimationGroup(*lols, run_time=0.2))

        lols = []
        for k in range(3 * (N // 4), N):
            color_range(k, 3 * (N // 4), right_col, going_right=True)
        for k in range(3 * (N // 4), N):
            lols.append(self.array[k].animate.set_color(WHITE))
        self.play(AnimationGroup(*lols, run_time=0.2))


        def show_example(i, j, c):
            self.q1 = MathTex(f"m({i}, {j})").shift(DOWN * 2)
            self.q2 = MathTex(
                f"m({i}, {j})", "=", "min(", f"m({i}, {c-1})", ",", f"m({c}, {j})", ")"
            ).move_to(self.q1)
            self.q2[3].set_color(left_col)
            self.q2[5].set_color(right_col)
            self.q3 = MathTex(
                f"m({i}, {j})", "=", "min(", f"A_2[{i}]", ",", f"A_2[{j}]", ")"
            ).move_to(self.q1)
            self.q3[3].set_color(left_col)
            self.q3[5].set_color(right_col)

            self.play(Write(self.q1))
            anims = []
            for k in range(i, j + 1):
                anims.append(self.array[k].animate.set_color(GREEN))
            self.play(AnimationGroup(*anims, run_time=1.5))

            anims = []
            for k in range(i, j + 1):
                anims.append(
                    self.array[k].animate.set_color(left_col if k < c else right_col)
                )
            self.play(Transform(self.q1, self.q2), AnimationGroup(*anims, run_time=1.5))

            anims = []
            anims.append(self.a[i].animate.set_color(left_col))
            anims.append(self.a[j].animate.set_color(right_col))
            anims.append(self.a_txts[i].animate.set_color(left_col))
            anims.append(self.a_txts[j].animate.set_color(right_col))
            self.play(Transform(self.q1, self.q3), AnimationGroup(*anims, run_time=1.5))
            indi = lambda x: Wiggle(x, scale_value=1.5)
            self.play(indi(self.a[i]), indi(self.a_txts[i]))
            self.play(indi(self.a[j]), indi(self.a_txts[j]))
            
            self.q4 = MathTex(
                f"m({i}, {j})", "=", "min(", f"{min(self.nums[i: c])}", ",", f"{min(self.nums[c:j+1])}", ") = ", f"{min(self.nums[i:j+1])}"
            ).move_to(self.q1)
            self.q4[3].set_color(left_col)
            self.q4[5].set_color(right_col)
            self.play(Transform(self.q1, self.q4))
            
            anims = []
            anims.append(FadeOut(self.q1))
            anims.append(self.a[i].animate.set_color(WHITE))
            anims.append(self.a[j].animate.set_color(WHITE))
            anims.append(self.a_txts[i].animate.set_color(WHITE))
            anims.append(self.a_txts[j].animate.set_color(WHITE))
            for k in range(i, j + 1):
                anims.append(self.array[k].animate.set_color(WHITE))
            self.play(AnimationGroup(*anims, run_time=0.7))

        # show_example(1, 6, N // 4)
        show_example(8, 13, 3 * (N // 4))

    def a3(self):
        self.array = create_array(map(str, self.nums), show_index=True, sz=sz).shift(
            UP * 2
        )
        self.add(self.array)
        self.a = create_array([""] * N, sz=sz).next_to(self.array, DOWN)

        def get_x_between(l):
            return (
                self.array[l].get_center()[0] + self.array[l + 1].get_center()[0]
            ) / 2

        solid_line_x = map(get_x_between, [3, 7, 11])
        dashed_line_x = map(get_x_between, [1, 5, 9, 13])
        dashed_lines = []
        solid_lines = []

        top = UP * 2 * sz
        bottom = DOWN * sz
        for x in solid_line_x:
            solid_lines.append(
                Line(
                    self.array.get_center() + top + RIGHT * x,
                    self.a.get_center() + bottom + RIGHT * x,
                    color=c_col,
                )
            )
        self.play(*map(Create, solid_lines))
        self.wait(0.5)
        for x in dashed_line_x:
            dashed_lines.append(
                DashedLine(
                    self.array.get_center() + top + RIGHT * x,
                    self.a.get_center() + bottom + RIGHT * x,
                    color=c_col,
                )
            )

        self.play(*map(Create, dashed_lines))
        self.wait(0.5)
        self.a_label = MathTex("A_3").next_to(self.a, LEFT)
        self.play(FadeIn(self.a_label, self.a))
        self.wait(0.5)
        
        self.a_txts = [None] * N

        def color_range(k, mid, col, going_right):
            ll = min(k, mid)
            rr = max(k, mid)
            anims = []
            anims.append(self.a[k].animate.set_color(col))
            for l in range(ll, rr + 1):
                anims.append(self.array[l].animate.set_color(col))
            formula = MathTex(
                f"A_3[",
                f"{k}",
                f"]= m(",
                f"{ll}",
                ",",
                f"{rr})",
                font_size=DEFAULT_FONT_SIZE * sz * 1.5,
            ).next_to(self.a[k], DOWN * 4)
            formula[1].set_color(col)
            formula[3].set_color(c_col if going_right else col)
            formula[5].set_color(col if going_right else c_col)
            anims.append(FadeIn(formula))
            up_factor = UP * 1.5 * sz
            if not going_right:
                arrow = Arrow(
                    start=self.array[mid].get_center() + up_factor + RIGHT * sz,
                    end=self.array[k].get_center() + LEFT * sz * 0.8 + up_factor,
                    color=col,
                    max_tip_length_to_length_ratio=1000,
                    max_stroke_width_to_length_ratio=1000,
                    tip_length=0.25,
                    tip_shape=ArrowSquareTip,
                )
            else:
                arrow = Arrow(
                    start=self.array[mid].get_center() + up_factor + LEFT * sz,
                    end=self.array[k].get_center() + RIGHT * sz * 0.8 + up_factor,
                    color=col,
                    max_tip_length_to_length_ratio=1000,
                    max_stroke_width_to_length_ratio=1000,
                    tip_length=0.25,
                    tip_shape=ArrowSquareTip,
                )
            if k == mid:
                arrow = None
            elif abs(k - mid) == 1:
                anims.append(Create(arrow))
                self.og_arrow = arrow
            else:
                anims.append(Transform(self.og_arrow, arrow))
            self.play(AnimationGroup(*anims, run_time=0.5))
            val = min(self.nums[ll : rr + 1])
            self.a_txts[k] = Text(
                str(val), font_size=DEFAULT_FONT_SIZE * sz, color=col
            ).move_to(self.a[k][1].get_center() + self.a[k].get_center())
            self.play(Create(self.a_txts[k]))

            anims = []
            anims.append(self.a[k].animate.set_color(WHITE))
            anims.append(self.a_txts[k].animate.set_color(WHITE))
            # for l in range(ll, rr + 1):
            #     anims.append(self.array[l].animate.set_color(WHITE))
            anims.append(FadeOut(formula))
            self.play(AnimationGroup(*anims, run_time=0.2))
            self.wait(0.5)

        lols = []
        for k in range(1, -1, -1):
            color_range(k, 1, left_col, going_right=False)
        for k in range(1, -1, -1):
            lols.append(self.array[k].animate.set_color(WHITE))
        self.play(AnimationGroup(*lols, run_time=0.2))

        lols = []
        for k in range(2, 4):
            color_range(k, 2, right_col, going_right=True)
        for k in range(2, 4):
            lols.append(self.array[k].animate.set_color(WHITE))
        self.play(AnimationGroup(*lols, run_time=0.2))
            
        lols = []
        for k in range(5, 3, -1):
            color_range(k, 5, left_col, going_right=False)
        for k in range(5, 3, -1):
            lols.append(self.array[k].animate.set_color(WHITE))
        self.play(AnimationGroup(*lols, run_time=0.2))

        lols = []
        for k in range(6, 8):
            color_range(k, 6, right_col, going_right=True)
        for k in range(6, 8):
            lols.append(self.array[k].animate.set_color(WHITE))
        self.play(AnimationGroup(*lols, run_time=0.2))

        lols = []
        for k in range(9, 7, -1):
            color_range(k, 9, left_col, going_right=False)
        for k in range(9, 7, -1):
            lols.append(self.array[k].animate.set_color(WHITE))
        self.play(AnimationGroup(*lols, run_time=0.2))

        lols = []
        for k in range(10, 12):
            color_range(k, 10, right_col, going_right=True)
        for k in range(10, 12):
            lols.append(self.array[k].animate.set_color(WHITE))
        self.play(AnimationGroup(*lols, run_time=0.2))

        lols = []        
        for k in range(13, 11, -1):
            color_range(k, 13, left_col, going_right=False)
        for k in range(13, 11, -1):
            lols.append(self.array[k].animate.set_color(WHITE))
        self.play(AnimationGroup(*lols, run_time=0.2))
        
        lols = []
        for k in range(14, 16):
            color_range(k, 14, right_col, going_right=True)
        for k in range(14, 16):
            lols.append(self.array[k].animate.set_color(WHITE))
        self.play(AnimationGroup(*lols, run_time=0.2))
            

        def show_example(i, j, c):
            self.q1 = MathTex(f"m({i}, {j})").shift(DOWN)
            self.q2 = MathTex(
                f"m({i}, {j})", "=", "min(", f"m({i}, {c-1})", ",", f"m({c}, {j})", ")"
            ).move_to(self.q1)
            self.q2[3].set_color(left_col)
            self.q2[5].set_color(right_col)
            self.q3 = MathTex(
                f"m({i}, {j})", "=", "min(", f"A_3[{i}]", ",", f"A_3[{j}]", ")"
            ).move_to(self.q1)
            self.q3[3].set_color(left_col)
            self.q3[5].set_color(right_col)

            self.play(Write(self.q1))
            anims = []
            for k in range(i, j + 1):
                anims.append(self.array[k].animate.set_color(GREEN))
            self.play(AnimationGroup(*anims, run_time=1.5))

            anims = []
            for k in range(i, j + 1):
                anims.append(
                    self.array[k].animate.set_color(left_col if k < c else right_col)
                )
            self.play(Transform(self.q1, self.q2), AnimationGroup(*anims, run_time=1.5))

            anims = []
            anims.append(self.a[i].animate.set_color(left_col))
            anims.append(self.a[j].animate.set_color(right_col))
            anims.append(self.a_txts[i].animate.set_color(left_col))
            anims.append(self.a_txts[j].animate.set_color(right_col))
            self.play(Transform(self.q1, self.q3), AnimationGroup(*anims, run_time=1.5))
            indi = lambda x: Wiggle(x, scale_value=1.5)
            self.play(indi(self.a[i]), indi(self.a_txts[i]))
            self.play(indi(self.a[j]), indi(self.a_txts[j]))

            anims = []
            anims.append(FadeOut(self.q1))
            anims.append(self.a[i].animate.set_color(WHITE))
            anims.append(self.a[j].animate.set_color(WHITE))
            anims.append(self.a_txts[i].animate.set_color(WHITE))
            anims.append(self.a_txts[j].animate.set_color(WHITE))
            for k in range(i, j + 1):
                anims.append(self.array[k].animate.set_color(WHITE))
            self.play(AnimationGroup(*anims, run_time=0.7))

        show_example(5, 7, 6)
        # show_example(12, 15, 14)


class All(Scene):
    def get_arrow(self, k, i, j):
        going_right = i < j
        col = right_col if going_right else left_col
        if not going_right:
            arrow = Arrow(
                start=self.a[k][i].get_center() + RIGHT * sz * 0.8,
                end=self.a[k][j].get_center() + LEFT * sz * 0.7,
                color=col,
                max_tip_length_to_length_ratio=1000,
                max_stroke_width_to_length_ratio=1000,
                tip_length=0.15,
                tip_shape=ArrowSquareTip,
            )
        else:
            arrow = Arrow(
                start=self.a[k][i].get_center() + LEFT * sz * 0.8,
                end=self.a[k][j].get_center() + RIGHT * sz * 0.7,
                color=col,
                max_tip_length_to_length_ratio=1000,
                max_stroke_width_to_length_ratio=1000,
                tip_length=0.15,
                tip_shape=ArrowSquareTip,
            )
        return arrow

    def construct(self):
        self.nums = [6, 3, 1, 6, 2, 8, 5, 7, 9, 6, 7, 8, 9, 4, 7, 3]
        self.array = create_array(map(str, self.nums), show_index=True, sz=sz).shift(
            UP * 3
        )
        self.a = [None] * 4
        self.a[1] = create_array([""] * N, sz=sz, color=GREY).next_to(
            self.array, DOWN * 3.5
        )
        self.a[2] = create_array([""] * N, sz=sz, color=GREY).next_to(
            self.a[1], DOWN * 2
        )
        self.a[3] = create_array([""] * N, sz=sz, color=GREY).next_to(
            self.a[2], DOWN * 2
        )

        self.a_txt = [None] * 4
        # self.a_txt[0] = MathTex("A_0").next_to(self.array, LEFT)
        self.a_txt[1] = MathTex("A_1").next_to(self.a[1], LEFT)
        self.a_txt[2] = MathTex("A_2").next_to(self.a[2], LEFT)
        self.a_txt[3] = MathTex("A_3").next_to(self.a[3], LEFT)

        self.add(self.array)
        # self.add(*self.a[1:])
        # self.add(*self.a_txt[1:])
        level = [None] * 4
        level[1] = [self.get_arrow(1, 7, 0), self.get_arrow(1, 8, 15)]
        level[2] = [
            self.get_arrow(2, 3, 0),
            self.get_arrow(2, 4, 7),
            self.get_arrow(2, 11, 8),
            self.get_arrow(2, 12, 15),
        ]
        level[3] = [
            self.get_arrow(3, 1, 0),
            self.get_arrow(3, 2, 3),
            self.get_arrow(3, 5, 4),
            self.get_arrow(3, 6, 7),
            self.get_arrow(3, 9, 8),
            self.get_arrow(3, 10, 11),
            self.get_arrow(3, 13, 12),
            self.get_arrow(3, 14, 15),
        ]
        # self.add(*level1, *level2, *level3)
        
        for i in [1, 2, 3]:
            self.play(FadeIn(self.a_txt[i], self.a[i], *level[i]))
            self.wait(1)

        LOGN = 4

        # LEVEL 1
        bin_group = []
        for i in range(N):
            b = bin(i)[2:]
            # get last 4 char of b
            b = b[-LOGN:].zfill(LOGN)
            btxt = MathTex(*b, font_size=DEFAULT_FONT_SIZE * sz * 1).next_to(
                self.a[1][i], UP * sz
            )
            bin_group.append(btxt)
        self.add(*bin_group)

        anims = []
        for i in range(N):
            anims.append(
                bin_group[i][0].animate.set_color(left_col if i < N // 2 else right_col)
            )
        self.play(AnimationGroup(*anims, run_time=0.5))
        self.wait(1)
        self.play(FadeOut(*bin_group))

        # LEVEL 2
        bin_group = []
        for i in range(N // 2):
            b = bin(i)[2:]
            # get last 4 char of b
            b = b[-LOGN:].zfill(LOGN)
            btxt = MathTex(*b, font_size=DEFAULT_FONT_SIZE * sz * 1).next_to(
                self.a[2][i], UP * sz
            )
            bin_group.append(btxt)
        self.play(FadeIn(*bin_group))

        anims = []
        for i in range(N // 2):
            anims.append(bin_group[i][0].animate.set_color(BLACK))
        self.play(*anims)
        anims = []
        for i in range(N // 2):
            anims.append(
                bin_group[i][1].animate.set_color(
                    right_col if (i // 4) % 2 else left_col
                )
            )
        self.play(AnimationGroup(*anims, run_time=0.5))
        self.wait(1)
        self.play(FadeOut(*bin_group))

        for i in range(N // 2, N):
            b = bin(i)[2:]
            # get last 4 char of b
            b = b[-LOGN:].zfill(LOGN)
            btxt = MathTex(*b, font_size=DEFAULT_FONT_SIZE * sz * 1).next_to(
                self.a[2][i], UP * sz
            )
            bin_group.append(btxt)
        self.play(FadeIn(*bin_group[N // 2 :]))
        anims = []
        for i in range(N // 2, N):
            anims.append(bin_group[i][0].animate.set_color(BLACK))
        self.play(AnimationGroup(*anims, run_time=0.5))
        self.wait(1)
        anims = []
        for i in range(N // 2, N):
            anims.append(
                bin_group[i][1].animate.set_color(
                    right_col if (i // 4) % 2 else left_col
                )
            )
        self.play(AnimationGroup(*anims, run_time=0.5))

        for i in range(N // 2):
            bin_group[i][0].set_color(WHITE)
        anims = []
        for i in range(N // 2, N):
            anims.append(bin_group[i][0].animate.set_color(WHITE))
        self.play(AnimationGroup(*anims, run_time=0.5), FadeIn(*bin_group[: N // 2]))

        self.wait(1)
        self.play(FadeOut(*bin_group))

        # LEVEL 3
        bin_group = [None] * N
        for i in range(4, 8):
            b = bin(i)[2:]
            # get last 4 char of b
            b = b[-LOGN:].zfill(LOGN)
            btxt = MathTex(*b, font_size=DEFAULT_FONT_SIZE * sz * 1).next_to(
                self.a[3][i], UP * sz
            )
            btxt[0].set_color(GREY)
            btxt[1].set_color(GREY)
            btxt[2].set_color(right_col if ((i // 2) % 2) else left_col)
            btxt[3].set_color(GREY)
            bin_group[i] = btxt
        self.play(FadeIn(*bin_group[4:8]))
        self.wait(1)
        for i in range(N):
            if 4 <= i < 8:
                continue
            b = bin(i)[2:]
            # get last 4 char of b
            b = b[-LOGN:].zfill(LOGN)
            btxt = MathTex(*b, font_size=DEFAULT_FONT_SIZE * sz * 1).next_to(
                self.a[3][i], UP * sz
            )
            btxt[0].set_color(GREY)
            btxt[1].set_color(GREY)
            btxt[2].set_color(right_col if ((i // 2) % 2) else left_col)
            btxt[3].set_color(GREY)
            bin_group[i] = btxt
        self.play(FadeIn(*bin_group[:4], *bin_group[8:]))
        self.wait(1)
        self.play(FadeOut(*bin_group))

        i_txt = MathTex(
            r"5 &= ",
            r"0",
            r"101 \\ 11 &= ",
            r"1",
            r"011",
            font_size=DEFAULT_FONT_SIZE * 1,
        ).next_to(self.a[3], DOWN * 2 * sz)
        self.add(i_txt)
        self.wait(1)
        self.play(Indicate(self.array[5]), Indicate(self.array[11]))
        self.wait(0.5)
        self.play(
            i_txt[1].animate.set_color(left_col), i_txt[3].animate.set_color(right_col)
        )
        self.wait(1)
        self.play(Indicate(self.a_txt[1]))
        self.wait(1)
        self.play(FadeOut(i_txt))

        i_txt = MathTex(
            r"9 &= 1",
            r"0",
            r"01 \\ 13 &= 1",
            r"1",
            r"01",
            font_size=DEFAULT_FONT_SIZE * 1,
        ).next_to(self.a[3], DOWN * 2 * sz)
        self.play(FadeIn(i_txt))
        self.wait(1)
        self.play(Indicate(self.array[9]), Indicate(self.array[13]))
        self.wait(0.5)
        self.play(
            i_txt[1].animate.set_color(left_col), i_txt[3].animate.set_color(right_col)
        )
        self.wait(1)
        self.play(Indicate(self.a_txt[2]))
        self.wait(1)
        self.play(FadeOut(i_txt))

        i_txt = MathTex(
            r"5 &= 01",
            r"0",
            r"1 \\ 7 &= 01",
            r"1",
            r"1",
            font_size=DEFAULT_FONT_SIZE * 1,
        ).next_to(self.a[3], DOWN * 1.5)
        self.play(FadeIn(i_txt))
        self.wait(0.5)
        self.play(Indicate(self.array[5]), Indicate(self.array[7]))
        self.wait(0.5)
        self.play(
            i_txt[1].animate.set_color(left_col), i_txt[3].animate.set_color(right_col)
        )
        self.wait(0.4)
        self.play(Indicate(self.a_txt[3]))
        self.wait(0.4)

        xor_out = MathTex("XOR(5, 7) = 00", "1", "0", font_size=DEFAULT_FONT_SIZE * 1)
        xor_out[1].set_color(YELLOW)
        # align xor_out so that it is below i_txt and the right endpoint is at the right endpoint of i_txt
        xor_out.next_to(i_txt, DOWN * 1.5)
        xor_out.shift(RIGHT * (i_txt.get_right() - xor_out.get_right()))

        self.play(FadeIn(xor_out))
        self.wait(0.5)
        self.play(FadeOut(i_txt, xor_out))

        formula_txt = MathTex(r"k = \text{ leftmost 1 bit of } XOR(l, r)").next_to(
            self.a[3], DOWN * 3
        )
        formula2_txt = MathTex(r"m(L, R) = min(A_k[L], A_k[R])").next_to(formula_txt, DOWN)
        self.play(Write(formula_txt))
        self.wait(1)
        self.play(Write(formula2_txt))
        self.wait(1)
        self.play(FadeOut(formula_txt, formula2_txt))

        # COMPLEXITY ANALYSIS
        right_txt = MathTex("\log_2(N)-1", font_size=DEFAULT_FONT_SIZE * 0.4).next_to(
            self.a[2], RIGHT, buff=0.08
        )
        up_arrow = Arrow(
            right_txt.get_center(),
            self.a[1][-1].get_corner(UP + RIGHT)[1] * UP
            + UP * 0.4
            + RIGHT * right_txt.get_center()[0],
        )
        down_arrow = Arrow(
            right_txt.get_center(),
            self.a[3][-1].get_corner(DOWN + RIGHT)[1] * UP
            + DOWN * 0.4
            + RIGHT * right_txt.get_center()[0],
        )
        self.play(FadeIn(right_txt, up_arrow, down_arrow))

        self.wait(0.3)

        bottom_txt = MathTex("N").next_to(self.a[3], DOWN)
        right_arrow = Arrow(
            bottom_txt.get_center() + RIGHT * 0.2,
            self.a[3][-1].get_corner(DOWN + RIGHT)[0] * RIGHT
            + UP * bottom_txt.get_center()[1],
        )
        left_arrow = Arrow(
            bottom_txt.get_center() + LEFT * 0.2,
            self.a[3][0].get_corner(DOWN + LEFT)[0] * RIGHT
            + UP * bottom_txt.get_center()[1],
        )
        self.play(FadeIn(bottom_txt, right_arrow, left_arrow))

        pre_mem = MathTex(
            r"\text{Preprocessing Memory: }", r"\mathcal{O}(N\log(N))"
        ).next_to(bottom_txt, DOWN * 1.5)
        pre_time = MathTex(
            r"\text{Preprocessing Time: }", r"\mathcal{O}(N\log(N))"
        ).next_to(pre_mem, DOWN)
        pre_time[0].align_to(pre_mem[0], RIGHT)
        pre_time[1].align_to(pre_mem[1], LEFT)

        self.play(Write(pre_mem))
        self.play(Write(pre_time))
        self.play(FadeOut(pre_mem, pre_time))
        query_time = MathTex(r"\text{Query Time: }", r"\mathcal{O}(1)").next_to(
            bottom_txt, DOWN * 1.5
        )
        self.play(Write(query_time))
