# Assets

`php artisan vendor:publish --provider="JutiaDev\Category\CategoryServiceProvider"`

# Relationships

- All models using the `hasCategories` trait will have access to the following relation `$model->categories` that will fetch all categories associated to this `$model`
- All models using the `hasCategory` trait will have access to the following relation `$model->category` that will fetch the category associated to this `$model`

- You can fetch all models associated to a `$category` through `$category->{$relationshipName}`, where `$relationshipName` will be deduced by default from the model class
  - e.g. `$relationshipName` from Product model will be products therefore you can access it with `$category->products`, you can get the relationName of a model with the helper function `deduce_relationship_name_from_model(\App\Models\Product::class)`
  - You can customize the relationshipName by adding this variable (`protected string $relationshipName = 'customProducts';`) on the model that is using the `hasCategories` or `hasCategory` trait

# Migration

> When to re-run migrations of the category package using the `php artisan migrate_category:refresh`:
- Adding a new model that uses  either `hasCategory` or `hasCategories` trait 
- Changing the trait of a model that was using for example the `hasCategory` trait to `hasCategories` or the inverse
- Changing the value of `cascadeDelete` on one of the models that uses the `hasCategory` trait
- Removing either the `hasCategory` or `hasCategories` from a model that was using either one of them

### 1 - A note on the `cascadeDelete`
- By default `cascadeDelete` will be false on the model that is using the `hasCategory` trait, therefore the foreign key will be set to null when the associated category is deleted.
if you want the model to be deleted too then you'll need this variable on the model using the `hasCategory` trait: `protected bool $cascadeDelete = true;`

### 2 - Impact of re-running migrations
- The Categorizable table will be created only if any eloquent model start using the `hasCategories` trait and the table does not exist already
- The Categorizable table will be deleted if no model is using the `hasCategories` trait and the table already exist


- if a model switches from the `hasCategories` to the `hasCategory` trait then a new column referencing the category id (foreign key) will be added to the model.
however if the `Categorizable` table is not deleted (check above point) then data will remain in the `Categorizable` table


- If a model that was using the `hasCategories` trait no longer uses any of the category trait then the foreign key column referencing the category_id will be deleted
- If a model that was using the `hasCategories` trait switchs to the `hasCategories` trait then the foreign key column referencing the category_id will be deleted but all data will be migrated to the `categorizable` table that will be created if it does not exist already.

### 3 - what does `php artisan migrate_category:refresh`
>
>- php artisan migrate:refresh --path=/database/migrations/2021_11_13_000001_create_categorizable_table.php
>- php artisan migrate:refresh --path=/database/migrations/2021_11_13_000002_add_categories_foreign_key_to_related_models.php

# Resources

- https://towardsdatascience.com/4-types-of-tree-traversal-algorithms-d56328450846/#943c
- https://gist.github.com/tmilos/f2f999b5839e2d42d751


- https://www.sitepoint.com/hierarchical-data-database-2/
- https://book.cakephp.org/2/en/core-libraries/behaviors/tree.html
