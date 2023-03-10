import discord, block, blockchain
import commands.user as user

from commands.helper import today

filler = ['<', '>', '!', '@']
"""Exchanges user uwuCreds for (a) raffle ticket(s)"""
async def buy_ticket(ctx, amount, BLOCKCHAIN):
    """1. Blockchain will be evaluated, user cred/ticket total is checked
       2. Blockchain will be validated, new block will be added to the end of Blockchain"""
       
    """Read Blockchain and return user total"""
    id, name = ctx.author.id, ctx.author.name
    user_creds = user.totalCreds(id, BLOCKCHAIN)
    user_tickets = user.totalTickets(id, BLOCKCHAIN)
    
    """Check if User requested -1 to purchase all tickets"""
    total_cost = 0
    if amount < 1:
        count = 0 
        while True:
            cost = 1000 + 500*(user_tickets + count)
            if cost + total_cost < user_creds:
                total_cost += cost
                count += 1
            else: 
                amount = count
                break
    else:
        for i in range(amount):
            total_cost += 1000 + 500*(user_tickets + i)
            
    """Check if User has sufficient amount of uwuCreds"""
    if user_creds - total_cost > 0:
        
        """Generate new Block"""
        new_block1 = block.Block(
            user = id,
            name = name,
            timestamp = today(),
            description = f'Bought {amount} ticket(s)',
            data = -total_cost
        )
        
        new_block2 = block.Block(
            user = id,
            name = name,
            timestamp = today(),
            description = 'Ticket',
            data = amount
        )
        
        """Update Blockchain"""
        if BLOCKCHAIN.isChainValid() == False:
            print('The current Blockchain is not valid, performing rollback.')
            BLOCKCHAIN = blockchain.Blockchain()
    
        BLOCKCHAIN.addBlock(new_block1)
        BLOCKCHAIN.addBlock(new_block2)
        if BLOCKCHAIN.isChainValid():
            BLOCKCHAIN.storeChain()           
    
        """Return Message"""
        embed = discord.Embed(
            title = f'Buy Ticket',
            description = f'Poggerz! **+{amount}** ticket(s) were added to your *Wallet*!',
            color = 15697464    
        ).set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)
        
    else:
        embed = discord.Embed(
            title = f'Buy Ticket',
            description = f'Insufficient funds, you require **{total_cost}** uwuCreds!',
            color = 6053215    
        ).set_thumbnail(url='https://66.media.tumblr.com/2d52e78a64b9cc97fac0cb00a48fe676/tumblr_inline_pamkf7AfPf1s2a9fg_500.gif')
        embed.set_footer(text='@~ powered by UwUntu')
        await ctx.send(embed=embed)
        
"""Allow users to view 10 top users, does not display their total uwuCreds"""
async def leaderboard (ctx, BLOCKCHAIN):
    """1. Blockchain will be evaluated, User uwuCreds will be checked
       2. Blockchain will be evaluated, User tickets will be checked"""

    leaderboard = user.getTop(BLOCKCHAIN)
    print(leaderboard)
    desc = 'Here lists the most active students in UTC Delta Phi Lambda!\n\n'
    count = 1
    for member in leaderboard:
        if count == 1:
            desc += f'\u3000** #{count} ** \u3000\u3000 **{member[0]}** \u3000~({member[1]})\n'
            count += 1
            continue

        desc += f'\u3000** #{count} ** '
        if count > 9: desc += '\u3000\u2000'
        else: desc += '\u3000\u3000'
        desc += f'*{member[0]}*\n'
        count += 1
    
    """Return Message"""
    embed = discord.Embed(
        title = f'Leaderboard',
        description = desc,
        color = 6943230    
    ).set_thumbnail(url=ctx.guild.icon_url)
    embed.set_footer(text='@~ powered by UwUntu')
    await ctx.send(embed=embed)

"""Allow users to see the list of raffle participants"""
async def rafflelist (ctx, BLOCKCHAIN):
    """1. Blockchain will be evaluated, User uwuCreds will be checked
       2. Blockchain will be evaluated, User tickets will be checked"""

    id, name = ctx.author.id, ctx.author.name

    rafflelist = user.getRaffle(BLOCKCHAIN)
    user_creds = user.totalCreds(id, BLOCKCHAIN)
    user_tickets = user.totalTickets(id, BLOCKCHAIN)

    count_tickets = 0 
    total_cost = 0
    while True:
        cost = 1000 + 500*(user_tickets + count_tickets)
        if cost + total_cost < user_creds:
            total_cost += cost
            count_tickets += 1
        else: break
    
    desc = 'Here lists the participating rafflers, the next drawing is at the end of the Semester!\n\n'

    desc += '\u3000\u3000\u3000\u3000\u2000 # \u3000 Name\n'
    count = 1
    for member in rafflelist:
        if count == 1:
            desc += '\u3000** #%-2d ** \u3000\u3000 %3.0f \u3000 **%-20s**\n' % (count, member[1], member[0][:20])
        elif count > 1 and count < 10:
            desc += '\u3000** #%-2d ** \u3000\u3000 %3.0f \u3000 %-20s\n' % (count, member[1], member[0][:20])
        else: 
            desc += '\u3000** #%-2d ** \u3000\u2000 %3.0f \u3000 %-20s\n' % (count, member[1], member[0][:20])

        count += 1

    desc += f'\n\nYou can currently buy **{count_tickets}** tickets with **{user_creds}** uwuCreds! '
    desc += f'Your next ticket costs **{1000 + 500*user_tickets}**, Ganbatte!'

    """Return Message"""
    embed = discord.Embed(
        title = f'Current Raffle',
        description = desc,
        color = 6943230    
    ).set_thumbnail(url=ctx.guild.icon_url)
    embed.set_footer(text='@~ powered by UwUntu')
    await ctx.send(embed=embed)

