<template>
    <div class="container">
      <div class="row justify-content-center mb-3 text-center"> 
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label for="exampleRegion">Find your hikes!</label>
            <input type="Region" v-model="region" class="form-control" id="regionInput" aria-describedby="regionHelp" placeholder="Enter a region e.g. Stuttgart">
            <small id="infoSubmit" class="form-text text-muted">Using OpenStreetMap to find all hiking routes in the specified region.</small>
          </div>
          <b-button type="submit" class="btn btn-success btn-sm">Submit</b-button>
        </form>
      </div>
      <alert :message=errorMessage v-if="showErrorMessage"></alert>
      <div style="height: 60vh">
        <LMap ref="map" :zoom="zoom" :center="center">
          <LControlLayers ref="control"></LControlLayers>
          <LTileLayer :url="url" :attribution="attribution"></LTileLayer>
          <LGeoJson ref="geojson" v-if="showGeo" :geojson="geohikes" :options="options"></LGeoJson>
        </LMap>
      </div>
      <div>
        <md-table md-card md-alignment="left" v-if="showHikingTable">
          <md-table-toolbar>
            <h1 class="md-title">Hikes</h1>
          </md-table-toolbar>
          <md-table-row>
            <md-table-head md-numeric>ID</md-table-head>
            <md-table-head>Name</md-table-head>
            <md-table-head>Description</md-table-head>
            <md-table-head>Start</md-table-head>
            <md-table-head>End</md-table-head>
            <md-table-head>Website</md-table-head>
          </md-table-row>
          <md-table-row v-for="index in hiking_ids" :key="index">
            <md-table-cell md-numeric>{{ index }} </md-table-cell>
            <md-table-cell>{{ hiking_names[index] }}</md-table-cell>
            <md-table-cell>{{ hiking_descriptions[index] }}</md-table-cell>
            <md-table-cell>{{ hiking_starts[index] }}</md-table-cell>
            <md-table-cell>{{ hiking_ends[index] }}</md-table-cell>
            <md-table-cell><a :href="`${hiking_urls[index]}`" v-if="hiking_urls[index]">Link</a></md-table-cell>
        </md-table-row>
        </md-table>
      </div>
    </div>
</template>
      
<script>
import { LMap, LTileLayer, LGeoJson, LControlLayers } from "vue2-leaflet";
import axios from 'axios';
import Alert from './Alert.vue';

const API_URL = process.env.VUE_APP_API_URL

export default {
  name: "MapView",
  components: {
    LMap,
    LTileLayer,
    LGeoJson,
    LControlLayers,
    alert: Alert,
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
      hiking_ids: [],
      hiking_names: [],
      hiking_descriptions: [],
      hiking_starts: [],
      hiking_ends: [],
      hiking_urls: [],
      showHikingTable: false,
      showErrorMessage: false,
      errorMessage: "",
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
    initSubmit() {
      this.hiking_ids = [];
      this.hiking_names = [];
      this.hiking_descriptions = [];
      this.hiking_starts = [];
      this.hiking_ends = [];
      this.hiking_urls = [];
      this.showHikingTable = false;
      this.showErrorMessage = false;
      this.errorMessage = "";
    },
    handleSubmit() {
      // set all data to init values
      this.initSubmit();
      // make request for region
      axios.get(`${API_URL}hiking/${this.region}/`)
        .then((res) => {
          this.geohikes = res.data.routes;
          // move map tile to route bounds
          this.$refs.map.mapObject.flyToBounds(res.data.bounds, { padding: [20, 20] });
          // fill table of hikes
          this.fillHikeTable();
        })
        .catch((error) => {
          // eslint-disable-next-line
          this.showErrorMessage = true;
          this.errorMessage = error.response.data.message;
        });
    },
    fillHikeTable() {
      this.showGeo = true;
      this.showHikingTable = true;
      this.geohikes.features.forEach((feature, index) => {
        this.hiking_ids.push(index);
        var name = feature.properties.tags.name
        if (!name) {
          name = "unknown";
        }
        this.hiking_names.push(name);
        var description = feature.properties.tags.description;
        if (!description) {
          description = "unknown";
        }
        this.hiking_descriptions.push(description);
        this.hiking_starts.push(feature.properties.tags.from);
        this.hiking_ends.push(feature.properties.tags.to);
        this.hiking_urls.push(feature.properties.tags.website);
      });
    }
  },
  mounted() {
    // this.getMessage();
  },
};
</script>