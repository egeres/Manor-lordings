import manor


class Serf(manor.entity):

    def tick():
        pass

    actions = [
        manor.entity.serf.find_wood(),
        manor.entity.serf.get_wood(),
    ]


class Lording(manor.lording):

    def tick(self):

        # Serf management
        if self.resources.wood < 10:
            self.ents.serfs(0, self.ents.serfs.count // 2).get_wood()
            self.ents.serfs(self.ents.serfs.count // 2, 0).get_stone()
        else:
            self.ents.serfs().get_stone()

        self.ents.militia().guard()
        self.ents.militia().attack_nearestenemy()
        self.ents.militia().set_patrol(
            [
                (0, 0),
                (0, 10),
                (10, 10),
                (10, 0),
            ]
        )

        for i in self.ents.militia():
            if i.health > i.health_max // 2:
                i.attack_nearest()

        if self.resources.stone >= 10:
            self.buildings.new("house", (1, 1))
            self.buildings.new("house", self.buildings.castle.nearest_free())
            self.buildings.new("tower")

            t = self.buildings.towers("random")
            t = self.buildings.towers("get_highest")
            if t.upgrade.materials():
                t.upgrade()
