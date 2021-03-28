<template>
  <div style="height: 80vh">
    <form @submit.prevent="handleSubmit">
      <label>
        Region:
        <input type="Region" v-model="region"/>
      </label>
      <button type="submit">Submit</button>
    </form>

    <LMap ref="map" :zoom="zoom" :center="center">
      <LControlLayers ref="control"></LControlLayers>
      <LTileLayer :url="url" :attribution="attribution"></LTileLayer>
      <LGeoJson ref="geojson" v-if="showGeoNrw" :geojson="geonrw" :options="options"></LGeoJson>
    </LMap>
  </div>
</template>
      
<script>
import { LMap, LTileLayer, LGeoJson, LControlLayers } from "vue2-leaflet";
import axios from 'axios';
// import image from "../assets/dark-map-icon.jpg"
// import geojsondata from "../assets/route-berlin-muenich.json"
const API_URL = 'http://localhost:5000/motorways';

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
      center: [47.5322, 3.9482],
      bounds: null,
      attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, ' +
			'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
      geonrw: "",
      showGeoNrw: false,
      region: "",
      options: {
        style: function(feature) {
          if (feature.geometry.type == "LineString") {
            return {
              weight: 2,
              color: '#000000'
            }
          } else {
            return {
              weight: 4,
              color: '#FF0000'
            }
          }

        },
        onEachFeature: function onEachFeature(feature, layer) {
          layer.bindPopup(feature.properties.tags.ref);
          // alternative hovering
          // layer.on('mouseover', function (e) {
          //   this.openPopup();
          // });
          // layer.on('mouseout', function (e) {
          //     this.closePopup();
          // });
        }
      }
    };
  },
  methods: {
    // getMessage() {
    //   axios.get(path)
    //     .then((res) => {
    //       this.geonrw = res.data.motorways;
    //     })
    //     .catch((error) => {
    //       // eslint-disable-next-line
    //       console.error(error);
    //     });
    // },
    handleSubmit() {
      // Send data to the server

      axios.get(`${API_URL}/${this.region}/`)
        .then((res) => {
          // this.getBooks();
          this.geonrw = res.data.motorways;
          this.map = this.$refs.map;
          // this.center = [47.5322, 3.9482]
          // this.$refs.map.mapObject.setView(L.latLng(47.413220, -1.219482), 13);
          // this.$refs.map.mapObject.fitBounds(this.$refs.geojson.getBounds())
          this.showGeoNrw = true;
          console.log("success")
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
    },
  },
  mounted() {
    // this.getMessage();
  },
};
</script>