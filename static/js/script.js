  var frameworks = ['React', 'Angular', 'Vue', 'Hyperapp', 'Omi'];
  var ctx = document.getElementById('myChart');

  var myChart = new Chart(ctx, {
      type: 'doughnut',
      data: {
         labels: frameworks,
         datasets: [{
             label: 'Popular JavaScript Frameworks',
             data: stars
             }]
      },
      options: {
          maintainAspectRatio: false,
          responsive: false
       },
     });