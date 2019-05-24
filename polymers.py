from visual import *
import random

Kb = 1.38064852E-23


class Field:
    def __init__(self, L, poly_num, poly_len, T, show=False):
        """
        constructor
        :param L: L is a tupple (x,y,z) - size
        :param poly_num: num of polumers
        """
        self.T = T
        self.poly_num = poly_num
        self.poly_len = poly_len
        self.L = L
        self.field = [[[None for z in xrange(L[2])] for y in xrange(L[1])] for x in xrange(L[0])]
        self.polymers = [Polymer(self, self.poly_len, i) for i in xrange(self.poly_num)]
        print self.field
        self.timestep()
        print self.field

    def warp_pos(self, pos):
        """
        warps the position around the field.
        use: wall on vector-> use vector
        :param pos: pos vector
        :return: no
        """
        pos.x %= self.L[0]
        pos.y %= self.L[1]
        pos.z %= self.L[2]

    def timestep(self):
        T = 2
        dt = 0.0001
        t = 0
        while t < T:
            for polymer in self.polymers:
                polymer.step()
            T += dt


class Polymer:
    def __init__(self, field, N, i):
        """
        constructor
        :param field: Field object containing the polymer
        :param N: number of monomers
        """
        self.field = field
        self.N = N
        self.counter = 0
        self.monomers = []
        self.i = i
        self.place_polymer()

    def update_field(self, remove=None):
        if remove:
            remove.ball.visible = False
            self.field.field[int(remove.pos.x)][int(remove.pos.y)][int(remove.pos.z)] = None
            del remove
        for mono in self.monomers:
            self.field.field[int(mono.pos.x)][int(mono.pos.y)][int(mono.pos.z)] = mono

    def place_polymer(self):
        """
        placing the polymer on the field
        :return: no
        """
        while (True):
            head_pos = vector(random.randint(0, self.field.L[0]),
                              random.randint(0, self.field.L[1]),
                              random.randint(self.field.L[2], self.field.L[2]))
            self.field.warp_pos(head_pos)
            if self.field.field[int(head_pos.x)][int(head_pos.y)][int(head_pos.z)]:  # if occupied
                continue

            self.monomers = [Monomer(head_pos, True, self.i)]
            self.update_field()
            for i in range(self.N - 1):
                pos = self.direction(i, solid_Z_borders=True)
                if not pos:
                    break
                self.monomers.append(Monomer(pos, True, self.i))
                self.update_field()
            else:
                break

    def step(self):
        prev_center = self.monomers[self.N / 2].pos.z
        new_pos = self.direction()

        if new_pos:
            new_centre = self.monomers[self.N / 2 - 1].pos.z
            delta_e = self.calc_energy(prev_center, new_centre)
            if random.uniform(0.0, 1.0) < math.exp(-delta_e / self.field.T):
                removed = self.monomers.pop()
                self.monomers = [Monomer(new_pos, True, self.i)] + self.monomers
                self.update_field(remove=removed)
            else:
                pass

        else:
            self.monomers.reverse()
            self.update_field()
            new_pos = self.direction()
            if new_pos:
                new_centre = self.monomers[self.N / 2 + 1].pos.z
                delta_e = self.calc_energy(prev_center, new_centre)
                if random.uniform(0.0, 1.0) < math.exp(-delta_e / self.field.T):
                    removed = self.monomers.pop()
                    self.monomers = [Monomer(new_pos, True, self.i)] + self.monomers
                    self.update_field(remove=removed)
                else:

                    print "polymer can't move!"

        center = self.monomers[self.N / 2].pos.z
        if abs(prev_center - center) > 1:
            self.counter += (prev_center - center) / abs(prev_center - center)
            print self.counter

    def direction(self, i=0, solid_Z_borders=False):
        """
        returns new position
        :param i: the index of the monomer
        :return: None if blocked, new position (vector) otherwise.
        """
        directions = [vector(1, 0, 0), vector(-1, 0, 0),
                      vector(0, 1, 0), vector(0, -1, 0),
                      vector(0, 0, 1), vector(0, 0, -1)]
        pos = self.monomers[i].pos
        free_places = []
        for direction in directions:
            new = pos + direction
            if solid_Z_borders:
                if not 0 < new.z < self.field.L[2]:
                    print "couldn't create polymer beyond the borders"
                    continue
            self.field.warp_pos(new)
            if self.field.field[int(new.x)][int(new.y)][int(new.z)] is None:
                free_places.append(new)
        if len(free_places) == 0:
            return None

        new_pos = random.choice(free_places)
        # print "new pos:", new_pos
        return new_pos

    def calc_energy(self, prev_pos, new_pos):
        energy = 0
        delta_z = new_pos - prev_pos
        if delta_z == 1 or delta_z == -self.field.L[2] - 1:
            energy -= 1
        if delta_z == -1 or delta_z == self.field.L[2] - 1:
            energy += 1
        return energy


class Monomer():
    def __init__(self, pos, show, i):
        self.pos = pos
        self.i = i
        if show:
            if i == 0:
                self.ball = sphere(pos=self.pos, radius=0.5, color=color.cyan)
            if i == 1:
                self.ball = sphere(pos=self.pos, radius=0.5, color=color.magenta)
            if i == 2:
                self.ball = sphere(pos=self.pos, radius=0.5, color=color.green)

    def __repr__(self):
        return str(self.pos)


###########################################
arrow(pos=vector(0, 0, 0), axis=vector(0, 0, -20), shaftwidth=1)
f = Field(L=(1, 20, 20), poly_num=3, poly_len=3, T=1)
