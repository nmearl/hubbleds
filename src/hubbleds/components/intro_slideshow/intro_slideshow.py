from dataclasses import dataclass, field
import solara
from solara import Reactive
import reacton.ipyvuetify as rv

from astropy.coordinates import SkyCoord
import astropy.units as u

from ...widgets.exploration_tool import ExplorationTool

from ...utils import IMAGE_BASE_URL, GALAXY_FOV

image_location = IMAGE_BASE_URL + "/stage_intro/"

_titles = [
    "Our Place in the Universe",
    "Answering Questions with Data",
    "Astronomy in the early 1900s",
    "Explore the Cosmic Sky",
    "What are the Fuzzy Things?",
    "Spiral Nebulae and the Great Debate",
    "Henrietta Leavitt's Discovery",
    "Vesto Slipher and Spectral Data"
]

messier_coordinates = {
    "M1": { "coord": SkyCoord(83.633 * u.deg, 22.014 * u.deg, frame="icrs"), "fov": 500 * u.arcsec },
    "M13": { "coord": SkyCoord(250.4 * u.deg, 36.44 * u.deg, frame="icrs"), "fov": 1400 * u.arcsec },
    "M31": { "coord": SkyCoord(10.63 * u.deg, 41.17 * u.deg, frame="icrs"), "fov": 10000 * u.arcsec },
    "M42": { "coord": SkyCoord(83.82 * u.deg, -5.39 * u.deg, frame="icrs"), "fov": 9000 * u.arcsec },
    "M51": { "coord": SkyCoord(202.47 * u.deg, 47.195 * u.deg, frame="icrs"), "fov": 900 * u.arcsec },
    "M82": { "coord": SkyCoord(148.97 * u.deg, 69.68 * u.deg, frame="icrs"), "fov": 500 * u.arcsec },
}

@solara.component
def carousel_title(step, titles):
    with rv.Toolbar(color="warning", dense=True, ):
        with rv.ToolbarTitle():
            solara.Text(titles[step], classes=["toolbar-title"])


@solara.component
def ExplorationToolComponent(messier_object):
    tool = ExplorationTool.element()
    moves, set_moves = solara.use_state(0)

    def go_to_coordinates():
        if messier_object.value:
            coordinates = messier_coordinates.get(messier_object.value, None)
            if coordinates is None:
                return
            location = coordinates["coord"]
            fov = coordinates.get("fov", GALAXY_FOV)
            tool_widget = solara.get_widget(tool)
            tool_widget.go_to_coordinates(location, fov=fov, instant=moves >= 2)
            set_moves(moves + 1)

    solara.use_effect(go_to_coordinates, [messier_object.value])

    return tool


@solara.component
def IntroSlideshow():
    step, on_step = solara.use_state(0)
    messier_object = solara.use_reactive(None)

    @solara.lab.computed
    def index():
        return step + 1

    with rv.Carousel(
            v_model=step,
            on_v_model=on_step,
            value=step + 1,
            hide_delimiters=True,
            hide_delimiter_background=True,
            show_arrows=False,
            height="100%",
    ) as carousel:

        # Slide 0
        with rv.CarouselItem():
            carousel_title(step, _titles)

            with solara.ColumnsResponsive(12, large=[5, 7]):
                with solara.Column(align="center"):
                    solara.HTML(
                        unsafe_innerHTML=
                        """
                        <p>
                        Humans have always looked to the sky and wondered how we and our universe came to be. 
                        </p>
                        <p>
                        In this <b>Cosmic Data Story</b>, you will use authentic astronomical data to investigate the mysteries of our Universe. In particular, you will be answering these questions:
                        </p>
                        """,
                        classes=["padded-text"],
                    )

                    with solara.Card(style="background-color: #0D47A1"):
                        solara.HTML(
                            unsafe_innerHTML=
                            """
                            <p
                                class="my-3 text-center"
                            >
                                Has the universe always existed?
                            </p>
                            <p
                                class="my-3 text-center"
                            >
                                If not, how long ago did it form?
                            </p>                            
                            """,
                            classes=["intro-card-text"],
                        )

                with solara.Column(align="center"):
                    rv.Img(
                        src=image_location + "MilkyWayOverMountainsNASASTScILevay.jpg",
                        max_height=550,
                        contain=True,
                        alt="Colorful image of our Milky Way galaxy in the sky over a dark silhouette of mountains on the horizon.",
                    )
                    solara.Text(
                        "Our Milky Way galaxy over a mountain range. (Credit: NASA and STScI)",
                        classes=["caption"],
                        style="text-align: center",
                    )
        # Slide 1
        with rv.CarouselItem():
            carousel_title(step, _titles)

            with solara.Row():
                with solara.ColumnsResponsive(12, large=[7,5]):
                    with solara.Column(align="center"):
                        solara.HTML(
                            unsafe_innerHTML=
                            """
                                <p>
                                    When scientists collect data to answer questions no one has answered yet, there is no answer key in the back of some book. So, as you explore this data story, you will learn how to <b>evaluate the reliability</b> of your results. Are the data really good enough to support a conclusion? <b>How can you know?</b> 
                                </p>
                                <p>
                                    Just as scientists constantly must, you'll <b>determine what can be concluded</b> from the data at-hand, and <b>how much confidence</b> you can have in your conclusions.
                                </p>
                                <p>
                                    Let's get started.
                                </p>
                            """,
                        classes = ["padded-text"],                       
                        )

                    with solara.Column(align="center"):
                        with solara.ColumnsResponsive(6, large=12):
                            with solara.Column(align="center", classes=[]):
                                solara.HTML(
                                    unsafe_innerHTML=
                                    f"""
                                    <img
                                        src = '{ image_location }HST-SM4.jpeg'
                                        style = 'max-height: 250px;'
                                        alt = 'The Hubble Space Telescope against a dark background'
                                    />
                                    """
                                )
                            with solara.Column(align="center", classes=[]):
                                solara.HTML(
                                    unsafe_innerHTML=
                                    f"""
                                    <img
                                        src = '{ image_location }EdwinHubble.jpg'
                                        style = 'max-height: 250px;'
                                        alt = 'Astronomer Edwin Hubble holding an image of the Andromeda Galaxy'
                                    />
                                    """
                                )
                        solara.Text(
                            "The Hubble Space Telescope and Edwin Hubble, the astronomer it was named for. Hubble holds an image of the Andromeda Galaxy, for which the earliest recorded observation was made in 964 AD by Iranian scholar al-Sufi.",
                            classes=["caption", ],
                            style="text-align: center; max-width: 80%",
                        )        

                        # Slide 2
        with rv.CarouselItem():
            carousel_title(step, _titles)

            with solara.Row():
                with solara.ColumnsResponsive(12, large=[5, 7]):
                    with solara.Column(align="center"):
                        solara.HTML(
                            unsafe_innerHTML=
                            """
                            <p>
                            Imagine that you are an astronomer living in the <b>early 1900s</b>. You and your colleagues around the world, including Albert Einstein, would agree that the <b>universe is unchanging</b> and <b>everlasting.</b> In other words, you expect that the universe always has been and will be the way it is the way you see it now. This picture of an unchanging universe had rarely been questioned throughout human history, thanks in large part to <b>Aristotle</b>, who embraced perfection and permanence. 
                            </p>
                            """,
                            classes=["padded-text"],
                        )

                    with solara.Column(align="center"):
                        with solara.ColumnsResponsive(6, large=12):
                            with solara.Column(align="center", classes=[]):
                                solara.HTML(
                                    unsafe_innerHTML=
                                    f"""
                                    <img
                                        src = "{image_location}Astronomer_Edward_Charles_Pickering's_Harvard_computers.jpg"
                                        style = 'max-height: 300px;'
                                        alt = 'Eight women astronomers, wearing late 1800s clothing and hairstyles, are sitting or standing in a room. Some are observing astronomical images with magnifying glasses. Some are writing in notebooks.'
                                    />
                                    """
                                )
                                solara.Text(
                                    "Women astronomers at Harvard College Observatory in 1892, including Henrietta Leavitt (third from left), Williamina Fleming (standing), and Annie Jump Cannon (far right).",
                                    classes=["caption", ],
                                    style="text-align: center; max-width: 80%",
                                )
                            with solara.Column(align="center"):
                                with solara.Columns(6):
                                    with solara.Column(align="end"):
                                        solara.HTML(
                                            unsafe_innerHTML=
                                            f"""
                                            <img
                                                src = '{image_location}Einstein_1921_by_F_Schmutzer_-_restorationCropped.png'
                                                style = 'max-height: 150px;'
                                                alt = 'Portrait of Albert Einstein'
                                            />
                                            """
                                        )
                                    with solara.Column(align="start"):
                                        solara.HTML(
                                            unsafe_innerHTML=
                                            f"""
                                            <img
                                                src = '{image_location}AristotleSchoolOfAthensCutoutZoom.png'
                                                style = 'max-height: 150px;'
                                                alt = 'Cutout showing a small portion of a much larger, colorful paiting by Raphael depicting Aristotle wearing a blue robe.'
                                            />
                                            """
                                        )
                                solara.Text(
                                    "Left: Albert Einstein in 1921. Right: Aristotle, depicted in “The School of Athens,” painted by Raphael for the walls of the Vatican between 1509 and 1511. Both believed in an unchanging universe.",
                                    classes=["caption", ],
                                    style="text-align: center; max-width: 80%",
                                )

                                # Slide 3
        with rv.CarouselItem():
            carousel_title(step, _titles)

            with solara.Column():
                solara.HTML(
                    unsafe_innerHTML=
                    """
                    <p>
                        The frame below provides an <b>interactive view</b> of the night sky, using images from real observations.
                    </p>
                    <p>
                        The brighter band you see going diagonally across the frame (before you try the controls) is caused by stars and dust in our home galaxy, called the <b>Milky Way.</b>
                    </p>
                    <p>
                        You can explore this view and see what is in the night sky, as astronomers have been doing for centuries. <b>Pan</b> (click and drag) and <b>zoom</b> (scroll in and out) to see parts of the sky beyond this view.
                    </p>
                    """,
                    classes=["padded-text"],
                )

                with solara.Columns([8, 4]):
                    with solara.Column():
                        ExplorationTool.element()
                        solara.Text(
                            "Interactive view provided by WorldWide Telescope",
                            classes=["caption"],
                            style="text-align: center",
                        )
                    with solara.Column(align="center", gap="20px"):
                        with solara.ColumnsResponsive(12, large=[4, 8]):
                            with solara.Column():
                                rv.Chip(label=True, outlined=True, children=["Pan"])
                            with solara.Column():
                                solara.HTML(
                                    unsafe_innerHTML=
                                    """
                                    <b>click + drag</b><br>
                                    (or use <b>I-J-K-L</b> keys)
                                    """
                                )
                        with solara.ColumnsResponsive(12, large=[4, 8]):
                            with solara.Column():
                                rv.Chip(label=True, outlined=True, children=["Zoom"])
                            with solara.Column():
                                solara.HTML(
                                    unsafe_innerHTML=
                                    """
                                    <b>scroll in and out</b><br>
                                    (or use <b class="codeFont">Z-X</b> keys)
                                    """
                                )

        # Slide 4
        with rv.CarouselItem():
            carousel_title(step, _titles)

            def set_coords(key):
                messier_object.set(key)

            with solara.Column():
                solara.HTML(
                    unsafe_innerHTML=
                    """
                    <p>
                        As you explore the cosmic sky, you may see stars and fuzzy blobs called <b>nebulae</b>. In the 1700's, French astronomer Charles Messier cataloged as many nebulae as he could find. They are known as Messier Objects and are identified by their catalog number. For example, M13 represents the 13th Messier Object in the catalog.
                    </p>
                    <p>
                        Click on the buttons to the right to <b>view some Messier Objects</b>. (Fun fact: “nebula” means “cloud” or “fog” in Latin.)
                    </p>
                    """,
                    classes=["padded-text"],
                )

                with solara.Columns([2, 1]):
                    with solara.Column():
                        ExplorationToolComponent(messier_object)

                        solara.Text(
                            "Interactive view provided by WorldWide Telescope",
                            classes=["caption"],
                            style="text-align: center",
                        )

                    with solara.Column():
                        with solara.ColumnsResponsive(12, large=[6, 6]):
                            with solara.Column():
                                solara.Button(
                                    label="M1",
                                    color="warning",
                                    on_click=lambda: set_coords("M1"),
                                    outlined=messier_object.value == "M1"
                                )
                                solara.Button(
                                    label="M31",
                                    color="warning",
                                    on_click=lambda: set_coords("M31"),
                                    outlined=messier_object.value == "M31"
                                )
                                solara.Button(
                                    label="M51",
                                    color="warning",
                                    on_click=lambda: set_coords("M51"),
                                    outlined=messier_object.value == "M51"
                                )
                            with solara.Column():
                                solara.Button(
                                    label="M13",
                                    color="warning",
                                    on_click=lambda: set_coords("M13"),
                                    outlined=messier_object.value == "M13"
                                )
                                solara.Button(
                                    label="M42",
                                    color="warning",
                                    on_click=lambda: set_coords("M42"),
                                    outlined=messier_object.value == "M42"
                                )
                                solara.Button(
                                    label="M82",
                                    color="warning",
                                    on_click=lambda: set_coords("M82"),
                                    outlined=messier_object.value == "M82"
                                )

                                # Slide 5
        with rv.CarouselItem():
            carousel_title(step, _titles)

            with solara.Column():
                solara.HTML(
                    unsafe_innerHTML=
                    """
                    <p>
                        <b>M31</b> and <b>M51</b> are examples of a particular type of nebula that interested astronomers in the early 1900s. They were known as <b>spiral nebulae</b> because of their distinctive spiral shape. In 1920, there was a Great Debate between astronomers Harlow Shapley and Heber Curtis questioning whether the spiral nebulae were perhaps young solar systems being born within our Milky Way galaxy or were "island universes” beyond it.
                    </p>
                    <p>
                        While you view these spiral nebulae, ponder what you would need to know to determine if they are within the Milky Way or beyond it. (Don't worry if you don't know. You will learn in this Data Story.) 
                    </p>
                    """,
                    classes=["padded-text"],
                )

                with solara.Columns([2, 1]):
                    with solara.Column():
                        ExplorationToolComponent(messier_object)

                        solara.Text(
                            "Interactive view provided by WorldWide Telescope",
                            classes=["caption"],
                            style="text-align: center",
                        )

                    with solara.Column():
                        with solara.ColumnsResponsive(12, large=[6, 6]):
                            with solara.Column():
                                solara.Button(
                                    label="M1",
                                    color="warning",
                                    disabled=True
                                )
                                solara.Button(
                                    label="M31",
                                    color="warning",
                                    on_click=lambda: set_coords("M31"),
                                    outlined=messier_object.value == "M31"
                                )
                                solara.Button(
                                    label="M51",
                                    color="warning",
                                    on_click=lambda: set_coords("M51"),
                                    outlined=messier_object.value == "M51"
                                ) 
                            with solara.Column():
                                solara.Button(
                                    label="M13",
                                    color="warning",
                                    disabled=True
                                )
                                solara.Button(
                                    label="M42",
                                    color="warning",
                                    disabled=True
                                )
                                solara.Button(
                                    label="M82",
                                    color="warning",
                                    disabled=True,
                                )

                                # Slide 6
        with rv.CarouselItem():
            carousel_title(step, _titles)

            with solara.Column():
                solara.HTML(
                    unsafe_innerHTML=
                    """
                    <p>
                    Between 1907&#8211;1921, Harvard astronomer <b>Henrietta Leavitt</b> observed Cepheid variable stars in a nebula called the Small Magellanic Cloud (SMC). By analyzing changes in the Cepheid stars’ brightness over time, she discovered that <b>fainter Cepheids vary more slowly than brighter ones</b>, as shown in her graph below. This important discovery made it possible to determine distances to spiral nebulae and finally resolve the Shapley-Curtis Great Debate: it turned out that spiral nebulae are far beyond the Milky Way and constitute <b>individual galaxies</b> in their own right.
                    </p>
                    """,
                    classes=["padded-text"],
                )

            with solara.Columns([2, 1]):
                with solara.Column(align="center"):
                    rv.Img(
                        src=image_location + "Leavitt_at_work.jpg",
                        max_height=350,
                        contain=True,
                        alt="Photograph of Henrietta Leavitt writing in a notebook. Several other notes are open neatly around her desk.",
                    )
                    solara.Text(
                        "Astronomer Henrietta Swan Leavitt",
                        classes=["caption", ],
                        style="text-align: center; max-width: 100%",
                    )

                with solara.Column(align="center"):
                    rv.Img(
                        src=image_location + "Leavitt_Plate.png",
                        max_height=200,
                        contain=True,
                        alt="Photographic glass plate of the Small Magellenic Cloud. Handwritten markings are scattered around the plate, noting objects of interest.",
                    )
                    solara.Text(
                        "Glass plate showing Cepheid variable stars in Small Magellanic Cloud studied by Leavitt",
                        classes=["caption", ],
                        style="text-align: center; max-width: 100%",
                    )

                    rv.Img(
                        src=image_location + "HSLeavittHSCr13Fig2_1912.jpeg",
                        max_height=200,
                        contain=True,
                        alt="A graph depicting stellar magnitude on the y-axis and period in days on the x-axis. Two plots are shown that go from the bottom left to the upper right of the chart.",
                    )
                    solara.Text(
                        "Graph from Leavitt's 1912 paper showing the relationship between period and brightness of Cepheid variables.",
                        classes=["caption", ],
                        style="text-align: center; max-width: 100%",
                    )

                    # Slide 7
        with rv.CarouselItem():
            carousel_title(step, _titles)

            with solara.Columns([7, 5]):
                with solara.Column(align="center"):
                    solara.HTML(
                        unsafe_innerHTML=
                        """
                        <p>
                        Around this same time, astronomer <b>Vesto Slipher</b> observed spiral nebulae using a spectrograph. Spectrographs can reveal a lot about an object in space, like what the object is made of or how fast it is moving toward or away from the observer.
                        </p>
                        <p>
                        Recall that the prevailing view in the early 1900s was that the universe is unchanging and eternal. As a result, the dominant expectation was that distant spiral nebulae are either not moving at all, or if they are moving then they are moving randomly.
                        </p>
                        <p>
                        It’s time for you to collect some of your own data, form conclusions, and compare your conclusions to what Vesto Slipher found.
                        </p>
                        """,
                        classes=["padded-text"],
                    )

                with solara.Column(align="center"):
                    rv.Img(
                        src=image_location + "V.M.Slipher.gif",
                        max_height=400,
                        contain=True,
                        alt="Portrait of Vesto Slipher",
                    )
                    solara.Text(
                        "Astronomer Vesto Slipher",
                        classes=["caption", ],
                        style="text-align: center; max-width: 100%",
                    )

    rv.Divider(class_="mt-4")

    rv.Pagination(
        v_model=index.value,
        on_v_model=lambda i: on_step(i - 1),
        length=len(carousel.kwargs.get("children", [])),
        circle=True,
        class_="elevation-0",
        navigation_color="red",
    )
