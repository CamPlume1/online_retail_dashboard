import React from 'react';
import './stats.css';

const Stats = () => {
  return (
    <div className="stats">
      <div className="stat-item">In this dashboard we are representing __ transactions</div>
      <div className="stat-item">This Seller is operating across __ countries</div>
      <div className="stat-item">This seller has sold $$__ in total goods</div>
      <div className="stat-item">This seller has sold __ total units</div>
        <div className="stat-item">This Seller's top item in units sold is __</div>
        <div className="stat-item">This seller's top item by revenue is__</div>
    </div>
  );
};

export default Stats;
