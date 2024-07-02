<template>
  <v-dialog
      v-model="dialog"
      persistent
      max-width="1000px"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-btn
        v-bind="attrs"
        v-on="on"
        block
        color="secondary"
        elevation="2"
        @click.stop="() => { opened = true; dialog_opened_callback() }"
      >
        Spectrum tutorial
      </v-btn>
    </template>
    <v-card
      class="mx-auto"
      ref="content"
    >
      <v-toolbar
        color="secondary"
        dense
        dark
      >
        <v-toolbar-title
          class="text-h6 text-uppercase font-weight-regular"
        >
          Light and Spectra
        </v-toolbar-title>
        <v-spacer></v-spacer>
<!--        <speech-synthesizer-->
<!--          :root="() => this.$refs.content.$el"-->
<!--          :autospeak-on-change="step"-->
<!--          :speak-flag="dialog"-->
<!--          :selectors="['div.v-toolbar__title', 'div.v-card__text.black&#45;&#45;text', 'h3', 'p']"-->
<!--          />-->
        <span
          @click="
            () => {
              $emit('close');
              dialog = false;
              if (step === 8) {
                step = 0;
              }
            }
          "
        >
          <v-btn icon>
            <v-icon> mdi-close </v-icon>
          </v-btn>
        </span>
      </v-toolbar>

      <v-window
        v-model="step"
        style="height: 70vh;"
        class="overflow-auto"
      >
        <v-window-item :value="0"
          class="no-transition"
        >
          <v-card-text>
            <v-container>
              <v-row>
                <v-col
                  cols="6"
                  class="d-flex flex-column"
                  height="100%"
                  flat
                  tile
                >
                  <h3
                    class="mb-4"
                  >
                    Refraction and diffraction
                  </h3>
                  <div>
                    <v-card
                      class="mt-auto mb-4"
                      flat
                      color="cyan lighten-1"
                      light
                    >
                      <v-card-text
                        class="black--text"
                      >
                        A <b>spectrum</b> is created when you pass light from a source through a spectrograph. A <b>spectrograph</b> separates the light into its different colors (like a rainbow) and measures how much light there is at each color (i.e. wavelength).
                      </v-card-text>
                    </v-card>
                    <p>
                      Diffraction gratings and prisms &#8212; and raindrops, bubbles, and oil slicks &#8212; create spectra because they bend light of different colors by different amounts.
                    </p>
                    <p>
                      The figure illustrates light passing through a diffraction grating (1) and a prism (2).
                    </p>
                  </div>
                </v-col>
                <v-col
                  cols="4"
                  offset="1"
                >
                  <v-img
                    id="grating_and_prism"
                    class="mb-4 mx-a mt-n3"
                    contain
                    :src="`${image_location}/refraction_diffraction_spectra.png`"
                  ></v-img>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
        </v-window-item>

        <v-window-item :value="1" class="no-transition">
          <v-card-text>
            <v-container>
              <v-row>
                <v-col
                  cols="6"
                  class="d-flex flex-column"
                  height="100%"
                  flat
                  tile
                >
                  <h3
                    class="mb-4"
                  >
                    Spectrum images and graphs
                  </h3>
                  <div>
                    <p>
                      The graphics to the right show sample spectra for two different types of light bulbs.
                    </p>
                    <p>
                      The spectrum images (i.e. the wide bar above the blue data points in each graphic) show what the light from each bulb looks like when it is separated into its colors by the spectrograph.
                    </p>
                    <p>
                      The spectrum graphs (i.e. the blue data points in each graphic) represent how bright the light is at each specific wavelength.
                    </p>
                  </div>
                </v-col>
                <v-col cols="6">
                  <v-card
                    color="white"
                    light
                    outlined
                    class="mt-n3 pa-3"
                  >
                    <h4>Light spectrum for LED bulb</h4>
                    <v-img
                      class="mb-4 mx-a"
                      contain
                      :src="`${image_location}/LED_White_spectool.png`"
                    ></v-img>
                    <h4>Light spectrum for sodium vapor bulb</h4>
                    <v-img
                      class="mx-a"
                      contain
                      :src="`${image_location}/Sodium_Vapor_spectool.png`"
                    ></v-img>
                  </v-card>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
        </v-window-item>

        <v-window-item :value="2" class="no-transition">
          <v-card-text>
            <v-container>
              <v-row>
                <v-col
                  cols="6"
                  class="d-flex flex-column"
                  height="100%"
                  flat
                  tile
                >
                  <h3 class="mb-4">Interpreting spectrum graphs</h3>
                  <div>
                    <p>
                      Examine the highlighted regions in the graphics to the right.
                    </p>
                    <p>
                      At wavelengths where the spectrum graph has a
                      <b>high brightness</b> value, the spectrum
                      image is <b>brightly lit</b> at the
                      corresponding wavelengths.
                    </p>
                  </div>
                </v-col>
                <v-col cols="6">
                  <v-card
                    color="white"
                    light
                    outlined
                    class="mt-n3 pa-3"
                  >
                    <h4>Light spectrum for LED bulb</h4>
                    <v-img
                      class="mb-4 mx-a"
                      contain
                      :src="`${image_location}/LED_White_w_highlight_spectool.png`"
                    ></v-img>
                    <h4>Light spectrum for sodium vapor bulb</h4>
                    <v-img
                      class="mx-a"
                      contain
                      :src="`${image_location}/Sodium_Vapor_w_highlight_spectool.png`"
                    ></v-img>
                  </v-card>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
        </v-window-item>

        <v-window-item :value="3" class="no-transition">
          <v-card-text>
            <v-container>
              <v-row>
                <v-col
                  cols="6"
                  class="d-flex flex-column"
                  height="100%"
                  flat
                  tile
                >
                  <h3 class="mb-4">Interpreting spectrum graphs</h3>
                  <div>
                    <p>
                      Examine the highlighted regions in the graphics to the right.
                    </p>
                    <p>
                      At wavelengths where the spectrum graph has a
                      <b>low brightness</b> value, the spectrum
                      image is <b>dim</b> or
                      <b>dark</b> at the corresponding wavelengths.
                    </p>
                  </div>
                </v-col>
                <v-col cols="6">
                  <v-card
                    color="white"
                    light
                    outlined
                    class="mt-n3 pa-3"
                  >
                    <h4>Light spectrum for LED bulb</h4>
                    <v-img
                      class="mb-4 mx-a"
                      contain
                      :src="`${image_location}/LED_White_w_neghighlight_spectool.png`"
                    ></v-img>
                    <h4>Light spectrum for sodium vapor bulb</h4>
                    <v-img
                      class="mx-a"
                      contain
                      :src="`${image_location}/Sodium_Vapor_w_neghighlight_spectool.png`"
                    ></v-img>
                  </v-card>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
        </v-window-item>

        <v-window-item :value="4" class="no-transition">
          <v-card-text>
            <v-container>
              <v-row>
                <v-col
                  cols="6"
                >
                  <h3
                    class="mb-4"
                  >
                    How do spectra indicate a source's motion?
                  </h3>
                  <div>
                    <p>
                      Think about a firetruck racing down the street. Have you noticed how the pitch of the siren changes depending whether the truck is moving toward or away from you? When the truck is moving toward you, the siren’s pitch is higher. When the truck is moving away from you, the siren’s pitch is lower. The faster the truck is moving, the bigger the change in pitch.
                    </p>
                    <p>
                      This pitch change is due to a phenomenon called the <b>Doppler shift</b>, where the observed properties of a sound wave change due to the motion of the object emitting the sound.
                    </p>
                    <p>
                      So what does this have to do with light waves and spectra?
                    </p>
                  </div>
                </v-col>
                <v-col cols="6">
                  <v-card
                    color="white"
                    light
                    outlined
                    class="mt-n3 pa-3"
                  >
                    <h4>
                      Doppler shift
                    </h4>
                    <v-img
                      class="mx-a"
                      contain
                      :src="`${image_location}/siren_moving_white.png`"
                    ></v-img>
                  </v-card>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
        </v-window-item>

        <v-window-item :value="5" class="no-transition">
          <v-card-text>
            <v-container>
              <v-row>
                <v-col
                  cols="6"
                >
                  <h3
                    class="mb-4"
                  >
                    How do spectra indicate a source's motion?
                  </h3>
                  <div>
                    <p>
                      The same <b>Doppler shift</b> happens with <b>light waves</b> (and all other wave phenomena). But a light source has to be moving very fast for you to notice these changes!
                    </p>
                    <p>
                      When a light source moves <b>away from you</b>, you observe the light to have a <b>longer (redder)</b> wavelength than you would if the object were not moving. This effect is called <b>redshift</b>.
                    </p>
                    <p>
                      When a light source moves <b>toward you</b>, you observe the light to have a <b>shorter (bluer)</b> wavelength than you would if the object were not moving. This effect is called <b>blueshift</b>.
                    </p>
                  </div>
                </v-col>
                <v-col cols="6">
                  <v-card
                    color="white"
                    light
                    outlined
                    class="mt-n3 pa-3"
                  >
                    <h4>
                      Doppler shift
                    </h4>
                    <v-img
                      class="mx-a"
                      contain
                      :src="`${image_location}/doppler_shift_light_white.png`"
                    ></v-img>
                  </v-card>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
        </v-window-item>

        <v-window-item :value="6" class="no-transition">
          <v-card-text>
            <v-container>
              <v-row>
                <v-col>
                  <h3
                    class="mb-4"
                  >
                    How do we know the rest wavelength of the light?
                  </h3>
                  <div>
                    <p>
                      A key to using the Doppler shift to determine the velocity of an astronomical source is to know the wavelength of its light when it is <b>not moving</b>. (This is called the <b>rest wavelength</b> of light).
                    </p>
                    <p>
                      Luckily, elements emit and absorb light at specific wavelengths that are unique to those elements. These unique patterns provide “chemical fingerprints” that we can use to identify the presence of an element in an astronomical source (like a star or a gas cloud).
                    </p>
                    <p>
                      The spectrum images below show the pattern of emission lines that are produced by four different elements. The emission line patterns are unique to each element.
                    </p>
                  </div>
                </v-col>
              </v-row>
              <v-row>
                <v-col
                  offset="1"
                  cols="10"
                >
                  <v-card
                    color="white"
                    light
                    outlined
                    class="px-3"
                  >
                    <v-row>
                      <v-col
                        cols="2"
                        class="d-flex flex-column"
                        height="100%"
                      >
                        <v-img
                          class="mx-a"
                          contain
                          :src="`${image_location}/carbon_atom_model.png`"
                        ></v-img>
                        <v-img
                          class="mt-auto mx-a"
                          contain
                          :src="`${image_location}/nitrogen_atom_model.png`"
                        ></v-img>
                      </v-col>
                      <v-col cols="8">
                        <v-img
                          class="mx-a"
                          contain
                          :src="`${image_location}/stsci_spectrum_element_montage.jpg`"
                        ></v-img>
                      </v-col>
                      <v-col cols="2" class="d-flex flex-column" height="100%">
                        <v-row>
                          <v-col>
                            <v-img
                              class="mx-a"
                              contain
                              :src="`${image_location}/oxygen_atom_model.png`"
                            ></v-img>
                          </v-col>
                        </v-row>
                        <v-row>
                          <v-col>
                            <v-img
                              class="mt-auto mx-a"
                              contain
                              :src="`${image_location}/iron_atom_model.png`"
                            ></v-img>
                          </v-col>
                        </v-row>
                      </v-col>
                    </v-row>
                  </v-card>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
        </v-window-item>

        <v-window-item :value="7" class="no-transition">
          <v-card-text>
            <v-container>
              <v-row>
                <v-col
                  cols="6"
                  class="d-flex flex-column"
                  height="100%"
                  flat
                  tile
                >
                  <h3 class="mb-4">
                    Emission and absorption lines in spectra
                  </h3>
                  <div>
                    <p>
                      The top spectrum shows <b>emission lines</b> from a source containing hydrogen.
                    </p>
                    <p>
                      The bottom spectrum shows <b>absorption lines</b> due to hydrogen.
                    </p>
                    <p>
                      Notice that in both spectra, the emission and absorption lines are present at the same combination of wavelengths (i.e. hydrogen’s “chemical fingerprint”).
                    </p>
                  </div>
                  <v-card
                    class="mt-auto"
                    flat
                    color="secondary lighten-3"
                    light
                  >
                    <v-card-text
                      class="black--text"
                    >
                      Elements emit light at specific wavelengths, and they can also absorb light at the same wavelengths, depending on the conditions associated with a light source.
                    </v-card-text>
                  </v-card>
                </v-col>
                <v-col cols="6">
                  <v-card
                    color="white"
                    light
                    outlined
                    class="mt-n3 pa-3"
                  >
                    <h4>Hydrogen emission spectrum</h4>
                    <v-img
                      class="mb-4 mx-a"
                      contain
                      :src="`${image_location}/hydrogen_emission_spectool.png`"
                    ></v-img>
                    <h4>Hydrogen absorption spectrum</h4>
                    <v-img
                      class="mx-a"
                      contain
                      :src="`${image_location}/hydrogen_absorption_spectool.png`"
                    ></v-img>
                  </v-card>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
        </v-window-item>

        <v-window-item :value="8"
          class="no-transition"
        >
          <v-card-text>
            <v-container>
              <v-row>
                <v-col
                  cols="12"
                >
                  <h3 class="mb-4">
                    Rest vs. Observed Wavelengths
                  </h3>
                  <p>
                    Since we know the wavelengths emitted or absorbed by an element when it is not moving, we can use these <b>rest wavelengths</b> as a reference to compare against the <b>observed wavelengths</b> of the light when an object <em>is</em> moving.
                  </p>
                </v-col>
              </v-row>
              <v-row>
                <v-col
                  cols="12"
                  lg="10"
                  offset-lg="1"
                >
                  <v-card
                    color="white"
                    light
                    outlined
                    class="mt-n3 pa-3"
                  >
                    <div
                      class="pa-3"
                    >
                      <h4>
                        Looking for the H-&alpha; emission line
                      </h4>
                      <p>
                        The dotted line shows the rest wavelength of a hydrogen line known as <b>H-&alpha;</b> (pronounced "H alpha"). The solid line shows the observed wavelength of the H-&alpha; line.
                      </p>
                    </div>
                    <v-img
                      contain
                      :src="`${image_location}/restobs1_dotted.png`"
                    >
                    </v-img>
                  </v-card>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
        </v-window-item>

        <v-window-item :value="9"
          class="no-transition"
        >
          <v-card-text>
            <v-container>
              <v-row>
                <v-col
                  cols="12"
                >
                  <h3 class="mb-4">
                    Rest vs. Observed Wavelengths
                  </h3>
                  <p>
                    Since we know the wavelengths emitted or absorbed by an element when it is not moving, we can use these <b>rest wavelengths</b> as a reference to compare against the <b>observed wavelengths</b> of the light when an object <em>is</em> moving.
                  </p>
                </v-col>
              </v-row>
              <v-row>
                <v-col
                  cols="12"
                  lg="10"
                  offset-lg="1"
                >
                  <v-card
                    color="white"
                    light
                    outlined
                    class="mt-n3 pa-3"
                  >
                    <div
                      class="pa-3"
                    >
                      <h4>
                        Looking for the Mg I absorption line
                      </h4>
                      <p>
                        The dotted line shows the rest wavelength of a magnesium line known as <b>Mg I</b> (pronounced "magnesium one"). The solid line shows the observed wavelength of the Mg I line.
                      </p>
                    </div>
                    <v-img
                      contain
                      :src="`${image_location}/restobs2_dotted.png`"
                    >
                    </v-img>
                  </v-card>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
        </v-window-item>

        <v-window-item :value="10"
          class="no-transition"
          style="height: 100%;"
        >
          <v-card-text
            style="height: 100%;"
          >
            <v-container
              style="height: 100%;"
            >
              <v-row
                style="height: 100%;"
                align="center"
              >
                <v-col
                  class="pa-4 text-center my-auto"
                >
                  <v-img
                    class="mb-4"
                    contain
                    height="128"
                    src="https://www.pngrepo.com/png/211744/512/rocket-ship-launch-missile.png"
                  ></v-img>
                  <h3 class="text-h6 font-weight-light mb-2">
                    You're ready to start measuring galaxy velocities now.
                  </h3>
                  <span class="text-caption grey--text">Click the <b>SPECTRUM TUTORIAL</b> button again if you'd like to come back for a refresher.</span>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
        </v-window-item>
      </v-window>

      <v-divider></v-divider>

      <v-card-actions>
        <v-btn
          :disabled="step === 0"
          class="black--text"
          color="accent"
          depressed
          @click="step--"
        >
          back
        </v-btn>
        <v-spacer></v-spacer>
        <v-item-group v-model="step" class="text-center" mandatory>
          <v-item
            v-for="n in length"
            :key="`btn-${n}`"
            v-slot="{ active, toggle }"
          >
            <v-btn :input-value="active" icon @click="toggle">
              <v-icon
                color="secondary"
              >
                mdi-record
              </v-icon>
            </v-btn>
          </v-item>
        </v-item-group>
        <v-spacer></v-spacer>
        <v-btn
          v-if="step < 10"
          class="black--text"
          color="accent"
          depressed
          @click="step++;"
        >
          next
        </v-btn>
        <v-btn
          v-if="step >= 10"
          color="accent"
          class="black--text"
          depressed
          @click="
            () => {
              $emit('close');
              dialog = false;
              step = 0;
            }
          "
        >
          done
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style>
.no-transition {
  transition: none !important;
}

#grating_and_prism .v-image__image {
  border-radius: 4px;
}
</style>