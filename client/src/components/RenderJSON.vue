<template>
  <b-container fluid>
    <b-form-group label="Number of elements to fetch: " label-for="input-field-size">
      <b-input-group>
        <b-form-input @keyup.enter="getData" id="input-field-size" v-model="size"></b-form-input>
        <b-input-group-append>
          <b-button variant="primary" @click="getData">Fetch</b-button>
        </b-input-group-append>
      </b-input-group>
    </b-form-group>

    <b-form-group>
      <b-button variant="primary" v-b-toggle.filtersCollapse>Filter...</b-button>
    </b-form-group>
    <b-collapse id="filtersCollapse">
      <b-card>
        <b-form-group label="Number of elements per page: " label-for="input-field-perPage">
          <b-form-input id="input-field-perPage" v-model="perPage"></b-form-input>
        </b-form-group>
        <b-form-group label="Filter (supports regex)" label-for="input-field-filter">
          <b-input-group>
            <b-form-input
              v-model="filter"
              type="search"
              id="input-field-filter"
              placeholder="Type to search"
            ></b-form-input>
            <b-input-group-append>
              <b-button :disabled="!filter" @click="filter = ''">Clear</b-button>
            </b-input-group-append>
          </b-input-group>
        </b-form-group>
        <b-form-group>
          <b-form-checkbox v-model="caseInsensitive">Make search case insensitive</b-form-checkbox>
        </b-form-group>
        <b-form-group label="Filter on" description="Leave all unchecked to filter on all data">
          <b-form-checkbox-group v-model="filterOn">
            <b-form-checkbox value="timestamp">Timestamp</b-form-checkbox>
            <b-form-checkbox value="src_ip">Source IP</b-form-checkbox>
            <b-form-checkbox value="src_port">Source port</b-form-checkbox>
            <b-form-checkbox value="dest_ip">Destination IP</b-form-checkbox>
            <b-form-checkbox value="dest_port">Destination port</b-form-checkbox>
            <b-form-checkbox value="proto">Protocol</b-form-checkbox>
            <b-form-checkbox value="alert.signature">Signature</b-form-checkbox>
            <b-form-checkbox value="app_proto">Application protocol</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
      </b-card>
      <br />
    </b-collapse>
    <b-pagination v-model="currentPage" :total-rows="totalRows" :per-page="perPage"></b-pagination>
    <b-table
      :filterIncludedFields="filterOn"
      @filtered="onFiltered"
      :filter="searchRegex"
      :items="alerts"
      :per-page="perPage"
      :current-page="currentPage"
      striped
      hover
      :fields="fields"
      @row-clicked="onExpand"
    >
      <template v-slot:row-details="row" class="test">
        <div>
          <h3>Data</h3>
          <vue-json-pretty
            style="background: #1d262f; color: #57718e; overflow-wrap: anywhere;"
            :deep="1"
            :showLength="true"
            :data="row.item"
          ></vue-json-pretty>
        </div>
        <div
          style="overflow-wrap: anywhere;"
          v-if="row.item.payload !== undefined && row.item.payload !== ''"
        >
          <h3>Payload</h3>
          <vue-code-highlight
            style="overflow-wrap: anywhere"
            language="http"
          >{{ debase(row.item.payload) }}</vue-code-highlight>
        </div>
        <div v-if="row.item.http !== undefined">
          <div v-if="row.item.http.http_request_body !== undefined">
            <h3>HTTP request body</h3>
            <vue-code-highlight
              style="overflow-wrap: anywhere"
              language="http"
            >{{ debase(row.item.http.http_request_body) }}</vue-code-highlight>
          </div>
        </div>
        <div v-if="row.item.http !== undefined">
          <div v-if="row.item.http.http_response_body">
            <h3>HTTP response body</h3>
            <vue-code-highlight
              style="overflow-wrap: anywhere"
              language="html"
            >{{ debase(row.item.http.http_response_body) }}</vue-code-highlight>
          </div>
        </div>
      </template>
      <template v-slot:cell(src_ip)="row">
        <b-link
          target="_blank"
          :href="'https://www.virustotal.com/gui/ip-address/' + row.item.src_ip + '/detection'"
        >{{ row.item.src_ip }}</b-link>
      </template>
      <template v-slot:cell(dest_ip)="row">
        <b-link
          target="_blank"
          :href="'https://www.virustotal.com/gui/ip-address/' + row.item.dest_ip + '/detection'"
        >{{ row.item.dest_ip }}</b-link>
      </template>
    </b-table>
    <b-pagination v-model="currentPage" :total-rows="totalRows" :per-page="perPage"></b-pagination>
  </b-container>
</template>

<script>
import { component as VueCodeHighlight } from "vue-code-highlight";
import axios from "axios";
import VueJsonPretty from "vue-json-pretty";

const basePath = "/api";

export default {
  name: "RenderJSON",
  components: {
    VueCodeHighlight,
    VueJsonPretty
  },
  mounted() {
    this.totalRows = this.alerts.length;
  },
  computed: {
    searchRegex() {
      if (this.caseInsensitive === true) {
        return new RegExp(this.filter, "i");
      } else {
        return new RegExp(this.filter);
      }
    }
  },
  data() {
    return {
      fields: [
        {
          key: "timestamp",
          sortable: true,
          label: "Timestamp"
        },
        {
          key: "src_ip",
          sortable: true,
          label: "Source IP"
        },
        {
          key: "src_port",
          sortable: true,
          label: "Source port"
        },
        {
          key: "dest_ip",
          sortable: true,
          label: "Destination IP"
        },
        {
          key: "dest_port",
          sortable: true,
          label: "Destination port"
        },
        {
          key: "proto",
          sortable: true,
          label: "Protocol"
        },
        {
          key: "alert.signature",
          sortable: true,
          label: "Signature"
        }
      ],
      filter: "",
      filterOn: [],
      perPage: 10,
      currentPage: 1,
      size: 10,
      alerts: [],
      totalRows: 0,
      caseInsensitive: false, 
      expandedRow: null
    };
  },
  methods: {
    getData() {
      const path = basePath + "/eve?size=" + this.size;
      axios
        .get(path)
        .then(response => {
          this.alerts = response.data.alerts;
        })
        .catch(error => {
          console.log(error);
        });
    },
    onFiltered(filteredItems) {
      this.totalRows = filteredItems.length;
    },
    debase(b64Data) {
      return atob(b64Data);
    }, 
    onExpand (item, index) {
      if ((this.expandedRow !== null) && (this.expandedRow !== index)) {
        this.alerts[this.expandedRow]._showDetails = false
      }
      this.expandedRow = index
      this.$set(item, '_showDetails', !item._showDetails)
    }
  },
  created() {
    this.getData();
  }
};
</script>

<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
