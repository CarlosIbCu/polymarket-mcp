#!/usr/bin/env python3
"""Simple test script for the FastMCP server."""

import asyncio
import httpx
from polymarket_mcp.main import BASE_URL

async def test_polymarket_api():
    """Test the Polymarket API endpoints directly."""
    print("Testing Polymarket API connectivity...")
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Test list markets
            response = await client.get(f"{BASE_URL}/markets", params={"limit": 2})
            print(f"List markets status: {response.status_code}")
            
            if response.status_code == 200:
                markets = response.json()
                print(f"✅ Successfully fetched {len(markets)} markets")
                print(f"Markets type: {type(markets)}")
                
                if isinstance(markets, dict):
                    print(f"Markets dict keys: {list(markets.keys())}")
                    # Handle case where markets is wrapped in a data field
                    markets_list = markets.get('data', markets.get('markets', markets))
                    if isinstance(markets_list, list) and len(markets_list) == 0:
                        markets_list = [markets] if markets.get('condition_id') else []
                else:
                    markets_list = markets if isinstance(markets, list) else [markets]
                
                # Test get market if we have markets
                if markets_list and len(markets_list) > 0:
                    first_market = markets_list[0]
                    print(f"First market keys: {list(first_market.keys())}")
                    
                    # Check for possible ID fields
                    condition_id = first_market.get('condition_id')
                    question_id = first_market.get('question_id')
                    market_slug = first_market.get('market_slug')
                    
                    print(f"condition_id: {condition_id}")
                    print(f"question_id: {question_id}")
                    print(f"market_slug: {market_slug}")
                    print(f"Question: {first_market.get('question', 'N/A')[:100]}...")
                    
                    # Try to fetch market details using condition_id
                    if condition_id:
                        try:
                            market_response = await client.get(f"{BASE_URL}/markets/{condition_id}")
                            print(f"Get market by condition_id status: {market_response.status_code}")
                            if market_response.status_code == 200:
                                market_data = market_response.json()
                                print("✅ Successfully fetched market details by condition_id")
                            else:
                                print(f"Failed to fetch by condition_id: {market_response.text[:200]}")
                        except Exception as e:
                            print(f"Error with condition_id: {e}")
                    
                    print("✅ API connectivity test completed successfully")
                else:
                    print("⚠️ No markets in response")
            else:
                print(f"❌ Failed to fetch markets: {response.text}")
                
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_polymarket_api())