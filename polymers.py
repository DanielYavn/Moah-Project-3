from visual import *
import random


class Field:
    def __init__(self, L, poly_num, poly_len, show=False):
        """
        constructor
        :param L: L is a tupple (x,y,z) - size
        :param poly_num: num of polumers
        """
        self.poly_num = poly_num
        self.poly_len = poly_len
        self.L = L
        self.field = [[[None for z in xrange(L[2])] for y in xrange(L[1])] for x in xrange(L[0])]
        self.polymers = [Polymer(self, self.poly_len) for i in xrange(self.poly_num)]
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
        for polymer in self.polymers:
            polymer.step()


class Polymer:
    def __init__(self, field, N):
        """
        constructor
        :param field: Field object containing the polymer
        :param N: number of monomers
        """
        self.field = field
        self.N = N
        self.monomers = []
        self.place_polymer()

    def update_field(self, remove=None):
        if remove:
            self.field.field[int(remove.x)][int(remove.y)][int(remove.z)] = None
        for mono in self.monomers:
            self.field.field[int(mono.x)][int(mono.y)][int(mono.z)] = mono

    def place_polymer(self):
        """
        placing the polymer on the field
        :return: no
        """
        while (True):
            head_pos = vector(random.randint(0, self.field.L[0]),
                              random.randint(0, self.field.L[1]),
                              random.randint(0, self.field.L[2]))
            self.field.warp_pos(head_pos)
            if self.field.field[int(head_pos.x)][int(head_pos.y)][int(head_pos.z)]:  # if occupied
                continue

            self.monomers = [head_pos]
            self.update_field()
            for i in range(self.N - 1):
                pos = self.direction(i)
                if not pos:
                    break
                self.monomers.append(pos)
                self.update_field()
            else:
                break

    def step(self):
        print self.monomers
        new_pos = self.direction()
        if new_pos:
            removed = self.monomers.pop()
            self.monomers = [new_pos] + self.monomers
            self.update_field(remove=removed)

        else:
            self.monomers.reverse()
            self.update_field()
            new_pos = self.direction()
            if new_pos:
                removed = self.monomers.pop()
                self.monomers = [new_pos] + self.monomers
                self.update_field(remove=removed)

                print "reversed"
                print self.monomers
            print "exit"
            exit()


    def direction(self, i=0):
        """
        returns new position
        :param i: the index of the monomer
        :return: None if blocked, new position (vector) otherwise.
        """
        directions = [vector(1, 0, 0), vector(-1, 0, 0),
                      vector(0, 1, 0), vector(0, -1, 0),
                      vector(0, 0, 1), vector(0, 0, -1)]
        pos = self.monomers[i]
        free_places = []
        for direction in directions:
            new = pos + direction
            self.field.warp_pos(new)
            if self.field.field[int(new.x)][int(new.y)][int(new.z)] is  None:
                free_places.append(new)
        if len(free_places) == 0:
            return None

        new_pos = random.choice(free_places)
        #print "new pos:", new_pos
        return new_pos


class Monomer:
    def __init__(self, pos):
        self.pos = pos


###########################################

f = Field((1, 2, 2), 2, 1)
