<?php

namespace JutiaDev\Category;

use Illuminate\Filesystem\Filesystem;
use Illuminate\Support\Collection;
use Illuminate\Support\ServiceProvider;
use JutiaDev\Category\Console\Commands\RefreshMigrationCommand;
use JutiaDev\Category\Contracts\Category as CategoryContract;
use JutiaDev\Category\Models\Category as CategoryModel;

class CategoryServiceProvider extends ServiceProvider
{
    /**
     * @param Filesystem $filesystem
     *
     * @throws \ReflectionException
     */
    public function boot(Filesystem $filesystem)
    {
        $this->loadRoutesFrom(__DIR__ . '/Routes/api.php');
        $this->loadMigrationsFrom(__DIR__ . '/../database/migrations');
        $this->loadTranslationsFrom(__DIR__ . '/../translations', 'category');

        if (function_exists('config_path')) { // function not available and 'publish' not relevant in Lumen
            $this->publishes(
                [
                    __DIR__ . '/../config/category.php' => config_path(
                        'category.php'
                    ),
                ],
                'config'
            );

            $this->publishes(
                [
                    __DIR__ . '/../translations' => resource_path(
                        'lang/vendor/category'
                    ),
                ],
                'translations'
            );
        }

        $this->registerCommands();

        $this->registerModelBindings();

        $this->registerModelRelationships();
    }

    public function register()
    {
        $this->mergeConfigFrom(
            __DIR__ . '/../config/category.php',
            'category'
        );
    }

    /**
     * Returns existing migration file if found, else uses the current
     * timestamp.
     *
     * @param Filesystem $filesystem
     *
     * @return string
     */
    protected function getMigrationFileName(Filesystem $filesystem): string
    {
        $timestamp = date('Y_m_d_His');

        /** @var ServiceProvider $this */
        return Collection::make(
            $this->app->databasePath() . DIRECTORY_SEPARATOR . 'migrations'
            . DIRECTORY_SEPARATOR
        )->flatMap(
            function ($path) use ($filesystem) {
                return $filesystem->glob(
                    $path . '*_create_categories_table.php'
                );
            }
        )->push(
            $this->app->databasePath()
            . "/migrations/{$timestamp}_create_categories_table.php"
        )->first();
    }

    protected function registerModelBindings()
    {
        $model = $this->app->config['category.model'];

        if (!$model) {
            return;
        }

        $this->app->bind(CategoryContract::class, $model);
    }

    /**
     * Register relationships on the Category model
     *
     * @return void
     * @throws \ReflectionException
     */
    protected function registerModelRelationships()
    {
        process_category_related_models(function ($associatedModel) {
            $this->setupRelationshipsForModel($associatedModel);
        });
    }

    private function registerCommands()
    {
        if ($this->app->runningInConsole()) {
            $this->commands([
                RefreshMigrationCommand::class,
            ]);
        }
    }

    private function setupRelationshipsForModel(string $modelClass)
    {
        $relationship = $this->getRelationshipType($modelClass);

        if (isset($relationship)) {
            $modelReflection = new $modelClass;
            $relationshipName = $modelReflection->getRelationshipName();
            $relationshipName = $relationshipName === null ? deduce_relationship_name_from_model($modelClass)
                : $relationshipName;

            CategoryModel::resolveRelationUsing(
                $relationshipName,
                function (CategoryModel $categoryModel) use (
                    $modelClass,
                    $relationship
                ) {
                    if ($relationship === 'belongsToMany') {
                        // A Many to Many Polymorphic Relationships
                        return $categoryModel->morphedByMany(
                            $modelClass,
                            'categorizable'
                        );
                    } else {
                        // A One to Many relationship
                        return $categoryModel->hasMany(
                            $modelClass,
                            $categoryModel->getForeignKey(),
                            $categoryModel->getKeyName(),
                        );
                    }
                }
            );
        }
    }

    private function getRelationshipType(string $modelClass): ?string
    {
        if (is_model_using_categories_trait($modelClass)) {
            $relationship = 'belongsToMany';
        } elseif (is_model_using_category_trait($modelClass)) {
            $relationship = 'hasMany';
        } else {
            $relationship = null;
        }

        return $relationship;
    }

}
