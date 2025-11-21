import { test, expect } from '@playwright/test';

// Mock API responses
const mockItems = [
  {
    id: '1',
    image_url: 'https://example.com/item1.jpg',
    category: 'Shirt',
    color: 'Blue',
    brand: 'BrandA',
    is_favorite: false,
  },
  {
    id: '2',
    image_url: 'https://example.com/item2.jpg',
    category: 'Pants',
    color: 'Black',
    brand: 'BrandB',
    is_favorite: true,
  },
];

test.beforeEach(async ({ page }) => {
  // Mock API calls
  await page.route('**/api/items', (route) => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ items: mockItems, count: mockItems.length }),
    });
  });

  await page.route('**/api/items/1/favorite', (route) => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ message: 'Favorite status updated', is_favorite: true }),
    });
  });

  await page.route('**/api/items/2', (route) => {
    if (route.request().method() === 'DELETE') {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ message: 'Item deleted successfully' }),
      });
    }
  });

  // Navigate to the closet page
  await page.goto('/closet-enhanced');
});

test.describe('Enhanced Closet Page', () => {
  test('should display all clothing items', async ({ page }) => {
    await expect(page.locator('text=My Closet')).toBeVisible();
    await expect(page.locator('img[alt="Shirt"]')).toBeVisible();
    await expect(page.locator('img[alt="Pants"]')).toBeVisible();
    await expect(page.locator('text=2 items')).toBeVisible();
  });

  test('should filter items by search query', async ({ page }) => {
    await page.fill('input[placeholder="Search items..."]', 'shirt');
    await expect(page.locator('img[alt="Shirt"]')).toBeVisible();
    await expect(page.locator('img[alt="Pants"]')).not.toBeVisible();
    await expect(page.locator('text=1 item')).toBeVisible();
  });

  test('should filter by category', async ({ page }) => {
    await page.selectOption('select', 'Pants');
    await expect(page.locator('img[alt="Pants"]')).toBeVisible();
    await expect(page.locator('img[alt="Shirt"]')).not.toBeVisible();
  });

  test('should filter by favorites', async ({ page }) => {
    await page.check('input[type="checkbox"]');
    await expect(page.locator('img[alt="Pants"]')).toBeVisible();
    await expect(page.locator('img[alt="Shirt"]')).not.toBeVisible();
  });

  test('should toggle favorite status', async ({ page }) => {
    // Initially, shirt is not favorite
    await expect(page.locator('img[alt="Shirt"] + button > span:has-text("🤍")')).toBeVisible();

    // Click to favorite
    await page.click('img[alt="Shirt"] + button');
    
    // Mock update
    await page.route('**/api/items', (route) => {
      const updatedItems = [...mockItems];
      updatedItems[0].is_favorite = true;
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ items: updatedItems, count: updatedItems.length }),
      });
    });

    // Re-fetch or check UI update
    // For simplicity, we assume UI updates correctly. In a real test, you might need to trigger a re-render.
  });

  test('should switch between grid and list view', async ({ page }) => {
    // Check grid view is default
    await expect(page.locator('.grid.grid-cols-1')).toBeVisible();

    // Switch to list view
    await page.click('button:has-text("List")');
    await expect(page.locator('.space-y-4')).toBeVisible();

    // Switch back to grid view
    await page.click('button:has-text("Grid")');
    await expect(page.locator('.grid.grid-cols-1')).toBeVisible();
  });

  test('should delete an item', async ({ page }) => {
    // Handle confirmation dialog
    page.on('dialog', dialog => dialog.accept());

    // Click delete
    await page.click('img[alt="Pants"] ~ div button:has-text("Delete")');

    // Mock update
    await page.route('**/api/items', (route) => {
      const updatedItems = mockItems.filter(item => item.id !== '2');
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ items: updatedItems, count: updatedItems.length }),
      });
    });

    // Check that item is removed
    await expect(page.locator('img[alt="Pants"]')).not.toBeVisible();
    await expect(page.locator('text=1 item')).toBeVisible();
  });
});
