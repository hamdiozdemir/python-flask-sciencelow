// SOME COLOURS ETC.
var barColors = [
  'rgba(255, 99, 132, 0.4)',
  'rgba(255, 159, 64, 0.4)',
  'rgba(255, 205, 130, 0.4)',
  'rgba(75, 192, 192, 0.4)',
  'rgba(54, 162, 235, 0.4)',
  'rgba(153, 102, 255, 0.4)',
  'rgba(201, 203, 207, 0.4)',
  'rgba(255, 99, 132, 0.4)',
  'rgba(180, 159, 64, 0.4)',
  'rgba(255, 130, 86, 0.4)',
  'rgba(75, 192, 88, 0.4)',
  'rgba(54, 162, 235, 0.4)',
  'rgba(200, 102, 200, 0.4)',
  'rgba(190, 99, 150, 0.4)',
  'rgba(230, 159, 99, 0.4)',
  'rgba(255, 205, 86, 0.4)',
  'rgba(75, 192, 192, 0.4)',
  'rgba(130, 162, 235, 0.4)',
  'rgba(153, 102, 200, 0.4)',

];

// CHART - Top 20 Keywords

fetch("/api/chart-data-top/")
.then(r => r.json())
.then(r => {
  new Chart("commonChart", {
    type: "bar",
    
    data: {
      
      labels: r.topKeys,
      datasets: [{
        backgroundColor: barColors,
        data: r.freqSum,
        hoverBorderWidth:5,
        label: "ALL"
      },
    {
      label: '2017',
      data: r.freq2017,
      type: 'line',
      fill: false,
      borderColor: 'rgba(0, 255, 0, 0.6)'

    },{
      label: "2018",
      data: r.freq2018,
      type: "line",
      fill: false,
      borderColor: 'rgba(0, 127, 255, 0.6)'
    },{
      label: "2019",
      data: r.freq2019,
      type: "line",
      fill: false,
      borderColor: 'rgba(170, 255, 170, 0.6)'
    },{
      label: "2020",
      data: r.freq2020,
      type: "line",
      fill: false,
      borderColor: 'rgba(255, 86, 255, 0.6)'
    },{
      label: "2021",
      data: r.freq2021,
      type: "line",
      fill: false,
      borderColor: 'rgba(0, 0, 180, 0.6)'
    },{
      label: "2022",
      data: r.freq2022,
      type: "line",
      fill: false,
      borderColor: 'rgba(0, 180, 130, 0.6)'
    }
  ]
    },
    options: {
      title: {
        display: true,
        text: "TOP 20 Keywords' Frequancies per Article Title"
      },
      legend:{
        display: true,
      },
      scales:{
        yAxes:[{
          ticks:{
            beginAtZero: true
          }
        }]
      }
  
  
    }
  });
})

// CHARTS - Categories
fetch("/api/chart-data-categories/")
.then(r => r.json())
.then(r=>{
  new Chart("allCategoryChart", {
    type: "bar",
    
    data: {
      
      labels: r.allKey,
      datasets: [{
        label:"Data",
        backgroundColor: barColors,
        data: r.allValue,
        hoverBorderWidth:5
      }]
    },
    options: {
      title: {
        display: true,
        text: "Frequancies per Category"
      },
      legend:{
        display: false,
      }
  
  
    }
  });

  new Chart("familyCategoryChart", {
    type: "bar",
    
    data: {
      
      labels: r.familyKey,
      datasets: [{
        // label:r.familyKey,
        backgroundColor: barColors,
        data: r.familyValue,
        hoverBorderWidth:5
      }]
    },
    options: {
      title: {
        display: true,
        text: "Frequancies per Family Category"
      },
      legend:{
        display: false,
      }
  
  
    }
  });

  new Chart("academicCategoryChart", {
    type: "bar",
    
    data: {
      
      labels: r.academicKey,
      datasets: [{
        backgroundColor: barColors,
        data: r.academicValue,
        hoverBorderWidth:5
      }]
    },
    options: {
      title: {
        display: true,
        text: "Frequancies per Academic Category"
      },
      legend:{
        display: false,
      }
  
  
    }
  });

  new Chart("senCategoryChart", {
    type: "bar",
    
    data: {
      
      labels: r.senKey,
      datasets: [{
        backgroundColor: barColors,
        data: r.senValue,
        hoverBorderWidth:5
      }]
    },
    options: {
      title: {
        display: true,
        text: "Frequancies per SEN(Special Education) Category"
      },
      legend:{
        display: false,
      },scales:{
        yAxes:[{
          ticks:{
            beginAtZero: true
          }
        }]
      }

  
  
    }
  });

  new Chart("wellbeingCategoryChart", {
    type: "bar",
    
    data: {
      
      labels: r.wellbeingKey,
      datasets: [{
        backgroundColor: barColors,
        data: r.wellbeingValue,
        hoverBorderWidth:5
      }]
    },
    options: {
      title: {
        display: true,
        text: "Frequancies per Wellbeing Category"
      },
      legend:{
        display: false,
      },
      scales:{
        yAxes:[{
          ticks:{
            beginAtZero: true
          }
        }]
      }
  
  
    }
  });

  new Chart("diversityCategoryChart", {
    type: "bar",
    
    data: {
      
      labels: r.diversityKey,
      datasets: [{
        backgroundColor: barColors,
        data: r.diversityValue,
        hoverBorderWidth:5
      }]
    },
    options: {
      title: {
        display: true,
        text: "Frequancies per Diversity Category"
      },
      legend:{
        display: false,
      },
      scales:{
        yAxes:[{
          ticks:{
            beginAtZero: true
          }
        }]
      }
  
  
    }
  });

  new Chart("digitalCategoryChart", {
    type: "bar",
    
    data: {
      
      labels: r.digitalKey,
      datasets: [{
        backgroundColor: barColors,
        data: r.digitalValue,
        hoverBorderWidth:5
      }]
    },
    options: {
      title: {
        display: true,
        text: "Frequancies per Digital Category"
      },
      legend:{
        display: false,
      },
      scales:{
        yAxes:[{
          ticks:{
            beginAtZero: true
          }
        }]
      }
  
  
    }
  });

  new Chart("attiduteCategoryChart", {
    type: "bar",
    
    data: {
      
      labels: r.attiduteKey,
      datasets: [{
        backgroundColor: barColors,
        data: r.attiduteValue,
        hoverBorderWidth:5
      }]
    },
    options: {
      title: {
        display: true,
        text: "Frequancies per Attidute Category"
      },
      legend:{
        display: false,
      },
      scales:{
        yAxes:[{
          ticks:{
            beginAtZero: true
          }
        }]
      }
  
  
    }
  });

  new Chart("othersCategoryChart", {
    type: "bar",
    
    data: {
      
      labels: r.othersKey,
      datasets: [{
        backgroundColor: barColors,
        data: r.othersValue,
        hoverBorderWidth:5
      }]
    },
    options: {
      title: {
        display: true,
        text: "Frequancies per Others Category"
      },
      legend:{
        display: false,
      },
      scales:{
        yAxes:[{
          ticks:{
            beginAtZero: true
          }
        }]
      }
  
  
    }
  });
})

// CHARTS - others
fetch("/api/chart-data/")
.then(q => q.json())
.then(r => {
  new Chart("journalChart", {
    type: "bar",
    
    data: {
      
      labels: r.journalList,
      datasets: [{
        label:"Data",
        backgroundColor: barColors,
        data: r.articleCount,
        hoverBorderWidth:5
      }]
    },
    options: {
      title: {
        display: true,
        text: "Articles per Journals"
      },
      legend:{
        display: false,
      }
  
  
    }
  });
  new Chart("quartileChart", {
    type: "pie",
    data: {
      labels: r.quartile_list,
      datasets: [{
        backgroundColor: barColors,
        data: r.quartile_num,
        hoverBorderWidth: 5
  
      }]
    },
    options: {
      title: {
        display: true,
        text: "Articles per Journal Quartile"
      }
      // hoverBackgroundColor: "black",
  
    }
  });

  new Chart("yearChart", {
    type: "line",
    data: {
      labels: r.articleYear,
      datasets: [{
        backgroundColor: "rgba(26,65,0,0.4)",
        borderColor: "rgba(0,180,230,0.4)",
        data: r.articleNum,
        fill: false,
        borderJoinStyle: "round",
        borderWidth: 7,
        pointBorderWidth: 10,

      }]
    },
    options:{
      title: {
        display: true,
        text: "Articles per Year"
      },
      legend:{
        display: false,
      },
      scales:{
        yAxes:[{
          ticks:{
            beginAtZero: true
          }
        }]
      }
      
    }
  });
})


// SEARCH CHART
new Chart("searchChart", {
  type: "bar",
  
  data: {
    
    labels: dataYear,
    datasets: [{
      backgroundColor: barColors,
      data: dataFreq,
      hoverBorderWidth:5
    }]
  },
  options: {
    title: {
      display: true,
      text: "Frequancies per Year"
    },
    legend:{
      display: false,
    },
    scales:{
      yAxes:[{
        ticks:{
          beginAtZero: true
        }
      }]
    }

  }
});


