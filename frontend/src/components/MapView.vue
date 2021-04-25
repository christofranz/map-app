<template>
  <!-- <div style="height: 80vh"> -->
    <div class="container">
      <div class="row justify-content-center mb-3">
        <!-- <b-form-select v-model="selected" :options="options_select" :select-size="4"></b-form-select>
        <div class="mt-3">Selected: <strong>{{ selected }}</strong></div> -->
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label for="exampleRegion">Find your hikes!</label>
            <input type="Region" v-model="region" class="form-control" id="regionInput" aria-describedby="regionHelp" placeholder="Enter a region e.g. Stuttgart">
            <small id="emailHelp" class="form-text text-muted">Using OpenStreetMap to find all hiking routes in the specified region.</small>
          </div>
          <b-button type="submit" class="btn btn-success btn-sm">Submit</b-button>
        </form>
      </div>
      <div style="height: 60vh">
        <LMap ref="map" :zoom="zoom" :center="center">
          <LControlLayers ref="control"></LControlLayers>
          <LTileLayer :url="url" :attribution="attribution"></LTileLayer>
          <LGeoJson ref="geojson" v-if="showGeo" :geojson="geohikes" :options="options"></LGeoJson>
        </LMap>
      </div>
    </div>
      

    
  <!-- </div> -->
</template>
      
<script>
import { LMap, LTileLayer, LGeoJson, LControlLayers } from "vue2-leaflet";
import axios from 'axios';

const API_URL = process.env.VUE_APP_API_URL

export default {
  name: "MapView",
  components: {
    LMap,
    LTileLayer,
    LGeoJson,
    LControlLayers
  },
  data() {
    return {
      url: "https://api.mapbox.com/styles/v1/mapbox/light-v9/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw",
      zoom: 6,
      center: [51.1642292, 10.4541194],
      bounds: null,
      attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, ' +
			'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
      geonrw: "",
      showGeo: false,
      region: "",
      geohikes: "",
      options: {
        style: function(feature) {
            return {
              weight: 3,
              color: feature.properties.color
            }
          },
        onEachFeature: function onEachFeature(feature, layer) {
          var content = feature.properties.tags.name
          if (!content) {
            content = "unknown";
          }
          var description = feature.properties.tags.description;
          var start_end = "From " + feature.properties.tags.from + " to " + feature.properties.tags.to;
          // var website = "Website: " + '<a href=' + feature.properties.tags.website + '>Link</a>';
          layer.bindPopup(content + '<br>' + start_end + '</br>' + description); // + '<br>' + website
          // alternative hovering
          layer.on('mouseover', function (e) {
            this.openPopup();
            e.target.setStyle({
            color: '#ff0033',
            });
          });
          layer.on('mouseout', function (e) {
              this.closePopup();
              e.target.setStyle({
                color: feature.properties.color
              });
          });
        }
      }
    };
  },
  methods: {
    handleSubmit() {
      // Send data to the server
      axios.get(`${API_URL}hiking/${this.region}/`)
        .then((res) => {
          this.geohikes = res.data.routes;
          // move map tile to route bounds
          this.$refs.map.mapObject.flyToBounds(res.data.bounds, { padding: [20, 20] });
          this.showGeo = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
    }
  },
  mounted() {
    // this.getMessage();
  },
};
</script>