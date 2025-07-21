import React from 'react';
import { PieChart, Pie, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, BarChart, Bar } from 'recharts';

const HealthMonitor = () => {
  // Vital Signs Data for Donut Chart
  const vitalSignsData = [
    { name: 'Heart Rate', value: 16.4, fill: '#92E0E5' },
    { name: 'Blood Pressure', value: 31.7, fill: '#5C9EAD' },
    { name: 'Body Temperature', value: 25.6, fill: '#326273' },
    { name: 'Respiratory Rate', value: 10.6, fill: '#2A4494' },
    { name: 'Oxygen Saturation', value: 15.8, fill: '#1D1D3B' }
  ];

  // Trend Data for Line Chart
  const trendData = [
    { name: 'Physical Activity', blue: 0, red: 5 },
    { name: 'Diet & Nutrition', blue: 27, red: 12 },
    { name: 'Stress Levels', blue: 15, red: 35 },
    { name: 'Posture & Ergonomics', blue: 30, red: 10 }
  ];

  // Daily Stats Data for Bar Chart
  const dailyStatsData = [
    { name: 'Day1', yellow: 6, pink: 5, blue: 5 },
    { name: 'Day2', yellow: 8, pink: 8, blue: 4 },
    { name: 'Day3', yellow: 15, pink: 10, blue: 5 },
    { name: 'Day4', yellow: 18, pink: 14, blue: 8 },
    { name: 'Day5', yellow: 22, pink: 20, blue: 8 }
  ];

  // Metrics Data
  const metricsData = [
    { label: 'Calorie Count', value: '50', bgColor: 'bg-lime-200' },
    { label: 'Weight', value: '70', bgColor: 'bg-green-200' },
    { label: 'Steps Count', value: '25', bgColor: 'bg-teal-600' },
    { label: 'cc', value: '30', bgColor: 'bg-teal-800' }
  ];

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <h1 className="text-3xl font-bold mb-8 text-gray-800">Health Monitor Dashboard</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Vital Signs Donut Chart */}
        <div className="bg-white p-4 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Vital Signs Distribution</h2>
          <PieChart width={400} height={300}>
            <Pie
              data={vitalSignsData}
              dataKey="value"
              nameKey="name"
              cx="50%"
              cy="50%"
              innerRadius={60}
              outerRadius={100}
              label
            />
            <Tooltip />
            <Legend />
          </PieChart>
        </div>

        {/* Trends Line Chart */}
        <div className="bg-white p-4 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Health Trends</h2>
          <LineChart width={400} height={300} data={trendData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="blue" stroke="#2A4494" />
            <Line type="monotone" dataKey="red" stroke="#FF0000" />
          </LineChart>
        </div>

        {/* Daily Stats Bar Chart */}
        <div className="bg-white p-4 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Daily Statistics</h2>
          <BarChart width={400} height={300} data={dailyStatsData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="yellow" fill="#FFD700" />
            <Bar dataKey="pink" fill="#FF69B4" />
            <Bar dataKey="blue" fill="#4169E1" />
          </BarChart>
        </div>

        {/* Metrics Grid */}
        <div className="bg-white p-4 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Key Metrics</h2>
          <div className="grid grid-cols-2 gap-4">
            {metricsData.map((metric, index) => (
              <div
                key={index}
                className={`${metric.bgColor} p-4 rounded-lg`}
              >
                <p className="text-gray-600 text-sm">{metric.label}</p>
                <p className="text-2xl font-bold">{metric.value}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default HealthMonitor;