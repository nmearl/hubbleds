<template>
  <scaffold-alert
    color="info"
    class="mb-4 mx-auto"
    max-width="800"
    elevation="6"
    title-text="Select your Galaxies"
    @back="back_callback()"
    @next="next_callback()"
    :can-advance="can_advance"
  >

  <template #before-next>
    <b>Select</b> {{ 5 - state_view.total_galaxies }} <span v-if="state_view.total_galaxies>0">more</span> <span v-if="state_view.total_galaxies < 4">galaxies</span><span v-if="state_view.total_galaxies == 4">galaxy</span>.
  </template>

    <div
      v-if="state_view.total_galaxies == 0 && !state_view.selected_galaxy"
      class="mb-4"
    >
      <p>
        The green dots in the Cosmic Sky Viewer mark the locations of galaxies you can collect data for. 
      </p>
      <p>
        Pan around the sky and click on one of these dots to select that galaxy.
      </p>
    </div>
    <div
      v-if="state_view.total_galaxies < 5 && state_view.selected_galaxy"
    >
      <p>
        If this galaxy looks good to you, click <v-btn icon dark x-small disabled class="mx-1 black--text" elevation="2" style="background-color: #00E676;"><v-icon style="color:black!important;">mdi-plus</v-icon></v-btn> to add it to your data set.
      </p>
      <p>
        If you’d rather look for another galaxy, click <v-btn icon dark x-small disabled class="mx-1 black--text" elevation="2" style="background-color: #00E676;"><v-icon style="color:black!important;">mdi-cached</v-icon></v-btn> to reset the view and choose a different green dot.
      </p>
    </div>
    <div
      v-if="state_view.total_galaxies == 1 && !state_view.selected_galaxy"
      class="mb-4"
    >
      <p>
        Choose another galaxy to enter into your table. You can pan around the sky from where you are or click the <v-btn icon dark small disabled class="mx-1 black--text" elevation="2" style="background-color: #00E676;"><v-icon style="color:black!important;">mdi-cached</v-icon></v-btn> button to reset the view.
      </p>
    </div>
    <div
      v-if="state_view.total_galaxies > 1 && state_view.total_galaxies < 5 && !state_view.selected_galaxy"
      class="mb-4"
    >
      <p>
        Check it out, your table is growing.
      </p>
      <p>
        Keep selecting galaxies until you have 5 rows in your table.
      </p>
    </div>
    <div
      v-if="state_view.total_galaxies == 5"
      class="mb-4"
    >
      <p>
        Great, you have all the galaxies that you need and you're now ready to begin making measurements from your data.
      </p>
      <p>
        Let's learn how to measure a galaxy's velocity using its light spectrum. 
      </p>
    </div>
  </scaffold-alert>
</template>

