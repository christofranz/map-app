<template>
  <div style="height: 80vh">
    <LMap :zoom="zoom" :center="center">
      <LControlLayers ref="control"></LControlLayers>
      <LTileLayer :url="url" :attribution="attribution"></LTileLayer>
      <LGeoJson :geojson="geonrw" :options="options"></LGeoJson>
    </LMap>
  </div>
</template>
      
<script>
import { LMap, LTileLayer, LGeoJson, LControlLayers } from "vue2-leaflet";
import axios from 'axios';
// import image from "../assets/dark-map-icon.jpg"
// import geojsondata from "../assets/route-berlin-muenich.json"

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
    getMessage() {
      const path = 'http://localhost:5000/motorways';
      axios.get(path)
        .then((res) => {
          this.geonrw = res.data.motorways;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  mounted() {
    this.getMessage();
  },
};
</script>