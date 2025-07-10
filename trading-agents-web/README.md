# Trading Agents Web App

A Next.js web application for the TradingAgents platform that allows users to upload CSV files or input stock tickers and get AI-powered trading recommendations.

## Features

- **Data Input**: Upload CSV files or enter stock ticker symbols
- **Agent Strategies**: Choose from 5 different trading strategies:
  - Conservative: Low risk, steady returns
  - Moderate: Balanced risk/reward
  - Aggressive: High risk, high potential returns
  - Momentum: Follow market trends
  - Value: Undervalued stock opportunities
- **AI Recommendations**: Get detailed trading recommendations with reasoning
- **Responsive Design**: Clean, mobile-friendly interface built with Tailwind CSS

## Getting Started

Since this is a scaffolded project with placeholder functions, you'll need to install dependencies first:

```bash
cd trading-agents-web
npm install
```

Then run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view the application.

## Project Structure

```
trading-agents-web/
├── app/
│   ├── globals.css          # Global styles with Tailwind
│   ├── layout.tsx           # Root layout component
│   └── page.tsx             # Homepage with all functionality
├── next.config.ts           # Next.js configuration
├── tailwind.config.ts       # Tailwind CSS configuration
├── tsconfig.json           # TypeScript configuration
└── package.json            # Dependencies and scripts
```

## Backend Integration

The current implementation includes placeholder functions for backend integration. To connect to your actual TradingAgents backend:

1. Replace the mock `handleRunAgents` function in `app/page.tsx`
2. Add your API endpoints for processing CSV files and ticker symbols
3. Update the `TradeResult` interface to match your backend response format
4. Add error handling and loading states as needed

## Customization

The app is designed to be easily customizable:

- **Styling**: Modify colors and design in `tailwind.config.ts` and component classes
- **Strategies**: Add or modify agent strategies in the dropdown options
- **Results Display**: Update the results section layout and information shown
- **Form Validation**: Add custom validation for CSV files and ticker inputs

## Built With

- [Next.js 15](https://nextjs.org/) - React framework
- [React 18](https://reactjs.org/) - UI library
- [TypeScript](https://www.typescriptlang.org/) - Type safety
- [Tailwind CSS](https://tailwindcss.com/) - Styling