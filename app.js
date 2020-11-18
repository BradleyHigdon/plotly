function buildCharts(sample) {

    d3.json(`/samples/${sample}`).then((data) => {
      const otu_ids = data.otu_ids;
      const otu_labels = data.otu_labels;
      const sample_values = data.sample_values;
      let bubbleLayout = {
        margin: { t: 0 },
        hovermode: "closests",
        xaxis: { title: "OTU ID"}
      }

      let bubbleData = [
        {
          x: otu_ids,
          y: sample_values,
          text: otu_labels,
          mode: "markers",
          marker: {
            size: sample_values,
            color: otu_ids,
          }
        }
      ]
  
      Plotly.plot("bubble", bubbleData, bubbleLayout);
  
      let pieData = [
        {
          values: sample_values.slice(0, 10),
          labels: otu_ids.slice(0, 10),
          hovertext: otu_labels.slice(0, 10),
          hoverinfo: "hovertext",
          type: "pie"
        }
      ];
      
      let pieLayout = {
        margin: { t: 0, l: 0 }
      };
  
      Plotly.plot("pie", pieData, pieLayout)
  })
  }