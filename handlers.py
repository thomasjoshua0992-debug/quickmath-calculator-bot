from telegram import Update
from telegram.ext import ContextTypes

from sympy import (
    sympify,
    solve,
    Symbol,
    sqrt,
    sin,
    cos,
    tan,
    log,
    pi,
    E,
)
from sympy.core.sympify import SympifyError


# Allowed mathematical functions and constants
SAFE_LOCALS = {
    "sqrt": sqrt,
    "sin": sin,
    "cos": cos,
    "tan": tan,
    "log": log,
    "pi": pi,
    "E": E,
}


def calculate_expression(expression: str):
    """Calculate a mathematical expression or solve an equation."""

    expression = expression.strip()

    if not expression:
        raise ValueError("Empty expression")

    # Allow ^ as an alternative to **
    expression = expression.replace("^", "**")

    # Solve an equation
    if "=" in expression:
        parts = expression.split("=")

        if len(parts) != 2:
            raise ValueError("Invalid equation")

        left, right = parts

        x = Symbol("x")

        left_side = sympify(
            left,
            locals=SAFE_LOCALS,
        )

        right_side = sympify(
            right,
            locals=SAFE_LOCALS,
        )

        equation = left_side - right_side

        return solve(equation, x)

    # Calculate normal expression
    return sympify(
        expression,
        locals=SAFE_LOCALS,
    )


async def start_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    """Handle /start."""

    text = (
        "🧮 *Welcome to QuickMath!*\n\n"
        "I can help you solve mathematical problems "
        "quickly and easily.\n\n"
        "📌 *Try these examples:*\n"
        "• `25 + 75`\n"
        "• `15 * 8`\n"
        "• `100 / 4`\n"
        "• `2^5`\n"
        "• `sqrt(144)`\n"
        "• `sin(pi/2)`\n"
        "• `x + 5 = 12`\n\n"
        "Simply send me your calculation.\n\n"
        "Use /help to see all available features."
    )

    await update.message.reply_text(
        text,
        parse_mode="Markdown",
    )


async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    """Handle /help."""

    text = (
        "📚 *QuickMath Help*\n\n"

        "🧮 *Basic calculations*\n"
        "`25 + 50`\n"
        "`100 - 35`\n"
        "`12 * 8`\n"
        "`144 / 12`\n\n"

        "📐 *Advanced calculations*\n"
        "`2^10`\n"
        "`sqrt(81)`\n"
        "`sin(pi/2)`\n"
        "`cos(0)`\n"
        "`log(100)`\n\n"

        "🔤 *Equations*\n"
        "`x + 5 = 15`\n"
        "`2*x = 20`\n"
        "`3*x + 2 = 14`\n\n"

        "📌 *Commands*\n"
        "/start - Start QuickMath\n"
        "/help - Show this help\n"
        "/calculate - Calculate an expression\n\n"

        "💡 You can also send a calculation "
        "directly without using a command."
    )

    await update.message.reply_text(
        text,
        parse_mode="Markdown",
    )


async def calculate_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    """Handle /calculate."""

    if not context.args:
        await update.message.reply_text(
            "❌ Please provide a calculation.\n\n"
            "Example:\n"
            "`/calculate 25 * 4`",
            parse_mode="Markdown",
        )
        return

    expression = " ".join(context.args)

    try:
        result = calculate_expression(expression)

        await update.message.reply_text(
            f"🧮 *Expression:*\n"
            f"`{expression}`\n\n"
            f"✅ *Answer:*\n"
            f"`{result}`",
            parse_mode="Markdown",
        )

    except (
        SympifyError,
        ValueError,
        TypeError,
        ZeroDivisionError,
    ):
        await update.message.reply_text(
            "❌ I couldn't understand that calculation.\n\n"
            "Try:\n"
            "`25 + 75`\n"
            "`sqrt(144)`\n"
            "`x + 5 = 12`",
            parse_mode="Markdown",
        )


async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    """Handle normal text calculations."""

    if not update.message:
        return

    if not update.message.text:
        return

    expression = update.message.text.strip()

    try:
        result = calculate_expression(expression)

        await update.message.reply_text(
            f"🧮 *Expression:*\n"
            f"`{expression}`\n\n"
            f"✅ *Answer:*\n"
            f"`{result}`",
            parse_mode="Markdown",
        )

    except (
        SympifyError,
        ValueError,
        TypeError,
        ZeroDivisionError,
    ):
        await update.message.reply_text(
            "❌ I couldn't calculate that.\n\n"
            "Please send a mathematical expression such as:\n\n"
            "`50 + 25`\n"
            "`12 * 8`\n"
            "`sqrt(100)`\n"
            "`x + 5 = 15`",
            parse_mode="Markdown",
  )
