from manim import *
import random


def create_textbox(text, sz=1, indx=None, show_index=False):
    box = Rectangle(width=sz, height=sz)
    text = Text(text, font_size=DEFAULT_FONT_SIZE * sz)
    text.move_to(box.get_center())
    grp = VGroup(box, text)
    if show_index:
        indx = Text(
            str(indx), font_size=DEFAULT_FONT_SIZE * sz * 0.65, weight=THIN
        ).next_to(box, DOWN * sz)
        grp.add(indx)
    return grp


def create_array(numbers, show_index=False, sz=1):
    textboxes = [
        create_textbox(num, sz, i, show_index=show_index)
        for i, num in enumerate(numbers)
    ]
    group = VGroup(*textboxes)
    group.arrange(RIGHT)
    return group


class Introduction(Scene):
    def do_example(self, i, j):
        t0 = (
            Text(f"m({i}, {j}) =", font_size=DEFAULT_FONT_SIZE * 0.8)
            .next_to(self.array1, DOWN * 2.5)
            .shift(LEFT * 1.5)
        )
        self.play(FadeIn(t0))
        l = lambda s: Text(s, font_size=DEFAULT_FONT_SIZE * 0.8).next_to(t0, RIGHT)
        t1 = l(f"min of index {i} to {j}")
        t2 = l(f"min({', '.join([str(num) for num in self.nums[i:j+1]])})")
        t3 = l(f"{min(self.nums[i:j+1])}")
        self.play(Create(t1))
        self.wait(1)
        anims = []
        for k in range(i, j + 1):
            anims.append(self.array1[k].animate.set_color(YELLOW))
        self.play(AnimationGroup(*anims, lag_ratio=0.5, run_time=1.5))
        self.wait(1)
        self.play(Transform(t1, t2))
        self.wait(1)
        self.play(Transform(t1, t3))
        self.play(
            Indicate(
                self.array1[self.nums.index(min(self.nums[i : j + 1]), i)], color=YELLOW
            )
        )
        anims = []
        for k in range(i, j + 1):
            anims.append(self.array1[k].animate.set_color(WHITE))
        self.play(AnimationGroup(*anims), FadeOut(t1), FadeOut(t0))

    def construct(self):
        title = Text("Range Minimum Query", font_size=DEFAULT_FONT_SIZE * 1.5).shift(
            UP * 2.6
        )
        N = 8
        self.nums = [random.randint(1, 9) for i in range(N)]
        print(self.nums)
        self.array1 = create_array(map(str, self.nums), show_index=True, sz=0.8).shift(
            UP * 0
        )
        self.add(title)
        self.play(Create(self.array1))

        self.do_example(3, 5)
        self.do_example(0, 4)


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
        self.nums = [random.randint(1, 9) for i in range(N)]
        self.array = create_array(
            map(str, self.nums), show_index=False, sz=sz / 1.33
        ).shift(UP * 3)
        self.grid = create_grid(N, sz).next_to(self.array, DOWN).shift(LEFT * 0.35)
        self.add(self.array)
        self.add(self.grid)

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
                        f"m({i},{j})", font_size=DEFAULT_FONT_SIZE * 0.5, color=BLUE
                    ).move_to(coord)
                )
                t1.append(
                    Text(
                        str(min(self.nums[i : j + 1])),
                        font_size=DEFAULT_FONT_SIZE * sz,
                        color=BLUE,
                    ).move_to(coord)
                )
        # self.add((VGroup(*t0)))
        m = VGroup(*t0)
        m1 = VGroup(*t1)
        self.play(Create(m))
        self.play(Transform(m, m1))


class Fast(Scene):
    def construct(self):
        N = 16
        sz = 0.5
        c_col = YELLOW
        left_col = RED
        right_col = BLUE
        self.nums = [random.randint(1, 9) for i in range(N)]
        self.array = create_array(map(str, self.nums), show_index=True, sz=sz).shift(UP)
        self.a = create_array([""] * N, sz=sz).next_to(self.array, DOWN)
        self.txt_c = MathTex("c = 8", font_size=DEFAULT_FONT_SIZE, color=c_col).next_to(
            self.array, UP * 6
        )

        self.add(self.array)
        self.add(self.txt_c)

        coords = self.array.get_center()
        print(coords)
        line = DashedLine(
            self.array.get_center() + UP * sz,
            self.a.get_center() + DOWN * sz,
            color=c_col,
        )
        self.add(line)
        self.add(self.a)

        self.a_txts = [None] * N

        for k in range(N // 2 - 1, -1, -1):
            # for k in [N//2 -1]:
            anims = []
            anims.append(self.a[k].animate.set_color(left_col))
            for l in range(k, N // 2):
                anims.append(self.array[l].animate.set_color(left_col))
            formula = MathTex(
                f"A[",
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
            for l in range(k, N // 2):
                anims.append(self.array[l].animate.set_color(WHITE))
            anims.append(FadeOut(formula))
            self.play(AnimationGroup(*anims, run_time=0.2))
            self.wait(0.5)

        for k in range(N // 2, N):
            # for k in [N//2 -1]:
            anims = []
            anims.append(self.a[k].animate.set_color(right_col))
            for l in range(N // 2, k + 1):
                anims.append(self.array[l].animate.set_color(right_col))

            formula = MathTex(
                f"A[",
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
            for l in range(N // 2, k + 1):
                anims.append(self.array[l].animate.set_color(WHITE))
            anims.append(FadeOut(formula))
            self.play(AnimationGroup(*anims, run_time=0.2))
            self.wait(0.5)

        i = 3
        j = 14
        c = N // 2
        self.q1 = MathTex("m(3, 14)").shift(DOWN * 2)
        self.q2 = MathTex(
            "m(3, 14)", "=", "min(", "m(3, 7)", ",", "m(8, 14)", ")"
        ).move_to(self.q1)
        self.q2[3].set_color(left_col)
        self.q2[5].set_color(right_col)
        self.q3 = MathTex("m(3, 14)", "=", "min(", "A[3]", ",", "A[14]", ")").move_to(
            self.q1
        )
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
            "i", r"\leq", "c", r"\leq", "j", font_size=DEFAULT_FONT_SIZE
        ).shift(DOWN * 2)
        self.txt_ij.set_color_by_tex("c", c_col)
        self.txt_ij.set_color_by_tex("i", left_col)
        self.txt_ij.set_color_by_tex("j", right_col)
        self.play(Write(self.txt_ij))

        self.q1 = MathTex("m(", "i", ",", "j", ")").next_to(self.txt_ij, DOWN)
        self.q1[1].set_color(left_col)
        self.q1[3].set_color(right_col)
        self.play(Write(self.q1))
        self.q2 = MathTex(
            "m(", "i", ",", "j", ")", "=", "min(", "m(i, c-1)", ",", "m(c, j)", ")"
        ).move_to(self.q1)
        self.q2[1].set_color(left_col)
        self.q2[7].set_color(left_col)
        self.q2[3].set_color(right_col)
        self.q2[9].set_color(right_col)
        self.q3 = MathTex(
            "m(", "i", ",", "j", ")", "=", "min(", "A[i]", ",", "A[j]", ")"
        ).move_to(self.q1)
        self.q3[1].set_color(left_col)
        self.q3[7].set_color(left_col)
        self.q3[3].set_color(right_col)
        self.q3[9].set_color(right_col)

        self.wait(0.5)
        self.play(Transform(self.q1, self.q2))
        self.wait(0.5)
        self.play(Transform(self.q1, self.q3))
