<template>
  <v-dialog
      v-model="dialog"
      persistent
      max-width="1000px"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-btn
        class="my-2"
        block
        color="secondary"
        elevation="2"
        id="hubble-exp-button"
        @click.stop="() => { dialog = true; }"
      >
        Hubble's Discovery
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
          {{ titles[step] }}
        </v-toolbar-title>
        <v-spacer></v-spacer>
        <!-- <speech-synthesizer
          :root="() => this.$refs.content.$el"
          :autospeak-on-change="step"
          :speak-flag="dialog"
          :selectors="['div.v-toolbar__title', 'div.v-card__text.black--text', 'h3', 'p']"
          /> -->
        <v-btn
          icon
          @click="closeDialog()"
          :disabled="maxStepCompleted < length - 1"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-toolbar>

        <v-window
          v-model="step"
          style="height: 70vh;"
          class="overflow-auto"
        >

        <v-window-item :value="0" class="no-transition">
          <v-card-text>
            <v-container>
              <v-row>
                <v-col>
                  <p>
                    The relationship between your galaxies’ velocity and distance is the same as what Hubble found: galaxies at a greater distance away are moving away from us at a higher velocity.
                  </p>
                  <p>
                    This was a <b>huge</b> deal in 1929. This relationship that Hubble found serves as evidence that we live in an <b>expanding universe</b>. Hubble realized that an expanding universe implies that at some point all the galaxies were much closer together — "<b>The Big Bang</b>". The amount of time since The Big Bang tells us the <b>age of the universe</b>.
                  </p>
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
                  cols = "12"
                  lg = "5"
                >
                  <p>
                    To understand Hubble’s thinking about this, let’s use the following situation as a model: Imagine runners in the middle of a race, where the runners are running at different speeds, as shown in the diagram.
                  </p>
                  <p>
                    Can you figure out how long ago the race started — the “age” of the race? (Assume each runner has maintained a consistent speed for the entire race).
                  </p>
                  <p>
                    The race began:
                  </p>
                  <mc-radiogroup
                    :radio-options="[
                      '1/3 of an hour ago',
                      '3 hours ago',
                      '12 hours ago',
                      '75 hours ago'
                    ]"
                    :feedbacks="[
                      'Try again. The age of the race is the distance any runner has traveled divided by their speed.',
                      'Correct. The age of the race is the distance any runner has traveled divided by their speed.',
                      'Try again. The age of the race is the distance any runner has traveled divided by their speed.',
                      'Try again. The age of the race is the distance any runner has traveled divided by their speed.',
                    ]"
                    :correct-answers="[1]"
                    @select="(option) => { if(option.correct) { this.maxStepCompleted = Math.max(this.maxStepCompleted, 1);} }"
                    score-tag="race-age"  
                  >
                  </mc-radiogroup>
                </v-col>
                <v-col
                  cols="12"
                  lg="7"
                >
                  <v-img
                    id="runners"
                    class="mb-4 mx-a mt-n3"
                    contain
                    :src="`${image_location}/runners_km.png`"
                  ></v-img>
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
                  cols="12"
                  lg="5"
                  >
                  <p>
                    To return to this data story, if we graph the runners’ velocities vs. distance, the graph would look like this.
                  </p>
                </v-col>
                <v-col
                  cols="12"
                  lg="7">
                  hubble_race_viewer goes here
                  <!-- <jupyter-widget :widget="hubble_race_viewer"/> -->
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
                  cols="12"
                  lg="5"
                  >
                  <p>
                    To return to this data story, if we graph the runners’ velocities vs. distance, the graph would look like this.
                  </p>
                </v-col>
                <v-col
                  cols="12"
                  lg="7">
                  hubble_race_viewer goes here
                  <!-- <jupyter-widget :widget="hubble_race_viewer"/> -->
                </v-col>
              </v-row>
              <v-row>
                <v-col
                  cols="12"
                  lg="5"
                  >
                  <p>
                    Doesn’t this look a lot like the trend in your class's graph for the galaxies?
                  </p>
                  <p>
                    As with the runners, you can use your galaxies’ velocity and distance data to calculate the time when all galaxies were in the same place — the <b>age of the universe</b>.
                  </p>
                  <p>
                    Let's learn how.
                  </p>
                </v-col>
                <v-col
                  cols="12"
                  lg="7">
                  layer_viewer goes here
                  <!-- <jupyter-widget :widget="layer_viewer"/> -->
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
        </v-window-item>

      </v-window>
      
      <v-divider></v-divider>

      <v-card-actions
        class="justify-space-between"
      >
        <v-btn
          :disabled="step === 0"
          class="black--text"
          color="accent"
          depressed
          @click="step--"
        >
          Back
        </v-btn>
        <v-spacer></v-spacer>
        <v-item-group
          v-model="step"
          class="text-center"
          mandatory
        >
          <v-item
            v-for="n in length"
            :key="`btn-${n}`"
            v-slot="{ active, toggle }"
          >
            <v-btn
              :disabled="n > maxStepCompleted + 2"
              :input-value="active"
              icon
              @click="toggle"
            >
              <v-icon>mdi-record</v-icon>
            </v-btn>
          </v-item>
        </v-item-group>
        <v-spacer></v-spacer>
          <v-btn
          :disabled="step > maxStepCompleted"
          v-if="step < length-1"
          color="accent"
          class="black--text"
          depressed
          @click="() => { step++; }"
        >
          {{ step < length-1 ? 'next' : '' }}
        </v-btn>
        <v-btn
          v-if = "step == length-1"
          color="accent"
          class="black--text"
          depressed
          @click="() => { $emit('close'); dialog = false; step = 0; on_slideshow_finished(); }"
        >
          Done
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  
  watch: {
    step(newStep) {
      const isInteractStep = this.interactSteps.includes(newStep);
      const newCompleted = isInteractStep ? newStep - 1 : newStep;
      // FIX: change this to a callback
      this.maxStepCompleted = Math.max(this.maxStepCompleted, newCompleted);
    },
  },

  methods: {
    closeDialog() {
      if (this.maxStepCompleted == this.length - 1) {
        this.$emit('close');
        this.dialog = false;
        if (this.step == this.length - 1) {
          this.step = 0;
        }
      }
    }
  }

  
};

</script>

<style>
.no-transition {
  transition: none;
}
</style>
