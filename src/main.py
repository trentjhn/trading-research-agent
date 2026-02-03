"""Main application entrypoint for the Trading Research Agent."""

import sys
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
import time

from src.agent import research_agent, ResearchState


def main():
    """Run the trading research agent from the command line."""
    console = Console()
    
    # Parse command line arguments
    if len(sys.argv) < 2:
        console.print(Panel(
            "[bold red]Error:[/bold red] Please provide a stock ticker.\n\n"
            "[bold]Usage:[/bold] python -m src.main [TICKER]\n\n"
            "[bold]Example:[/bold] python -m src.main AAPL",
            title="Trading Research Agent",
            border_style="red"
        ))
        sys.exit(1)

    ticker = sys.argv[1].upper()
    
    # Display header
    console.print()
    console.print(Panel(
        f"[bold cyan]Starting comprehensive research analysis for:[/bold cyan] [bold yellow]{ticker}[/bold yellow]\n\n"
        "[dim]Running 4 parallel analyses:[/dim]\n"
        "  • Fundamental Analysis (financials, valuation)\n"
        "  • Technical Analysis (price trends, indicators)\n"
        "  • Sentiment Analysis (news, market perception)\n"
        "  • Macroeconomic Analysis (market conditions)",
        title="🚀 Trading Research Agent",
        border_style="cyan"
    ))
    console.print()

    # Initialize state
    initial_state: ResearchState = {
        "ticker": ticker,
        "fundamental_analysis": "",
        "technical_analysis": "",
        "sentiment_analysis": "",
        "macro_analysis": "",
        "final_report": ""
    }

    # Run the agent with progress indicator
    start_time = time.time()
    
    try:
        console.print("[bold]Running parallel analyses...[/bold]\n")
        
        # Execute the graph (this will run all 4 analyses in parallel)
        final_state = research_agent.invoke(initial_state)
        
        elapsed_time = time.time() - start_time
        
        # Display success message
        console.print()
        console.print(f"[bold green]✓[/bold green] Analysis complete in {elapsed_time:.2f} seconds")
        console.print()
        
        # Display the final report
        console.print(Panel(
            f"[bold blue]Investment Report: {ticker}[/bold blue]",
            border_style="blue"
        ))
        console.print()
        
        # Render the markdown report
        md = Markdown(final_state['final_report'])
        console.print(md)
        console.print()
        
        # Display footer
        console.print(Panel(
            "[dim]This report is for informational purposes only and should not be considered financial advice.\n"
            "Always conduct your own research and consult with a qualified financial advisor before making investment decisions.[/dim]",
            border_style="dim"
        ))
        
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Analysis interrupted by user.[/yellow]")
        sys.exit(1)
        
    except Exception as e:
        console.print()
        console.print(Panel(
            f"[bold red]Error:[/bold red] {str(e)}\n\n"
            "[dim]Please check:\n"
            "  • The ticker symbol is valid\n"
            "  • Docker services are running (docker-compose up -d)\n"
            "  • Your ANTHROPIC_API_KEY is set in .env\n"
            "  • You have internet connectivity[/dim]",
            title="❌ Analysis Failed",
            border_style="red"
        ))
        sys.exit(1)


if __name__ == "__main__":
    main()

